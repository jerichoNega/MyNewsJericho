import yaml, requests, feedparser, datetime
from bs4 import BeautifulSoup
from database import SessionLocal
from models import Article
from rss_parser import RSSParser

def fast_fetch():
    db = SessionLocal()
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    parser = RSSParser(config['feeds'])
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    for feed in config['feeds']:
        print(f"--- Fetching: {feed['name']} ---")
        try:
            r = requests.get(feed['url'], headers=headers, timeout=10)
            p = feedparser.parse(r.text)
            
            count = 0
            for e in p.entries[:15]: # Limit to 15 per source for speed
                item_id = e.get('id') or e.get('link')
                if not item_id: continue
                
                if db.query(Article).filter(Article.external_id == item_id).first():
                    continue
                
                print(f"  Scraping: {e.title[:40]}...")
                img = parser._extract_image(e)
                
                a = Article(
                    external_id=item_id,
                    title=e.title,
                    source=feed['name'],
                    url=e.link,
                    summary=e.get('summary', e.get('description', '')),
                    image_url=img,
                    category=feed.get('category', 'General'),
                    published_at=datetime.datetime.now()
                )
                db.add(a)
                count += 1
            
            db.commit()
            print(f"  Added {count} articles.")
        except Exception as ex:
            print(f"  Error: {ex}")
            db.rollback()
    
    db.close()

if __name__ == "__main__":
    fast_fetch()
