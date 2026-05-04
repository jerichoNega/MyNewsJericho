import feedparser
import requests

class RSSParser:
    def __init__(self, feeds_config):
        self.feeds_config = feeds_config

    def fetch_new_entries(self, state_manager):
        new_entries = []
        headers = {'User-Agent': 'Mozilla/5.0 (MyNewsJericho Bot)'}
        for feed in self.feeds_config:
            print(f"Fetching feed: {feed['name']}...")
            try:
                response = requests.get(feed['url'], headers=headers, timeout=10)
                response.raise_for_status()
                parsed_feed = feedparser.parse(response.text)
                
                for entry in parsed_feed.entries:
                    # Use link or id as a unique identifier
                    item_id = entry.get('id') or entry.get('link')
                    
                    if item_id and state_manager.is_new(item_id):
                        new_entries.append({
                            'source': feed['name'],
                            'title': entry.get('title', 'No Title'),
                            'link': entry.get('link', ''),
                            'summary': entry.get('summary', entry.get('description', '')),
                            'id': item_id
                        })
            except Exception as e:
                print(f"Error fetching {feed['name']}: {e}")
        
        return new_entries
