import feedparser
import requests
from models import Article
from sqlalchemy.orm import Session
import datetime
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class RSSParser:
    def __init__(self, feeds_config):
        self.feeds_config = feeds_config

    def _extract_image(self, entry):
        # 1. Media RSS
        if 'media_content' in entry and entry.media_content:
            return entry.media_content[0]['url']
        if 'media_thumbnail' in entry and entry.media_thumbnail:
            return entry.media_thumbnail[0]['url']
        
        # 2. Enclosures
        if 'enclosures' in entry:
            for enc in entry.enclosures:
                if enc.get('type', '').startswith('image/'):
                    return enc['href']
        
        # 3. BeautifulSoup fallback from summary/content
        content = entry.get('summary', '') or entry.get('description', '')
        if 'content' in entry:
            content = entry.content[0].value
            
        if content:
            soup = BeautifulSoup(content, 'html.parser')
            img = soup.find('img')
            if img and img.get('src'):
                return urljoin(entry.get('link', ''), img['src'])

        # 4. Final Fallback: Scrape OpenGraph from URL
        try:
            url = entry.get('link')
            if url:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
                resp = requests.get(url, timeout=5, headers=headers)
                if resp.status_code == 200:
                    page_soup = BeautifulSoup(resp.text, 'html.parser')
                    og_image = page_soup.find('meta', property='og:image')
                    if og_image and og_image.get('content'):
                        return og_image['content']
                    
                    # Also check twitter:image
                    twitter_image = page_soup.find('meta', name='twitter:image')
                    if twitter_image and twitter_image.get('content'):
                        return twitter_image['content']
        except:
            pass
        
        return None

    def fetch_new_entries_to_db(self, db: Session):
        new_entries = []
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        for feed in self.feeds_config:
            print(f"Fetching feed: {feed['name']}...")
            try:
                response = requests.get(feed['url'], headers=headers, timeout=10)
                response.raise_for_status()
                parsed_feed = feedparser.parse(response.text)
                
                for entry in parsed_feed.entries:
                    item_id = entry.get('id') or entry.get('link')
                    
                    if not item_id:
                        continue
                        
                    exists = db.query(Article).filter(Article.external_id == item_id).first()
                    if not exists:
                        image_url = self._extract_image(entry)
                        
                        new_article = Article(
                            external_id=item_id,
                            title=entry.get('title', 'No Title'),
                            source=feed['name'],
                            url=entry.get('link', ''),
                            summary=entry.get('summary', entry.get('description', '')),
                            image_url=image_url,
                            category=feed.get('category', 'General'),
                            published_at=datetime.datetime.now()
                        )
                        db.add(new_article)
                        new_entries.append(new_article)
                
                db.commit()
            except Exception as e:
                print(f"Error fetching {feed['name']}: {e}")
                db.rollback()
        
        return new_entries
