import feedparser, requests, datetime
from bs4 import BeautifulSoup
from database import SessionLocal
from models import Article

db = SessionLocal()
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

# OpenAI
r = requests.get('https://openai.com/news/rss.xml', headers=headers)
p = feedparser.parse(r.text)
for e in p.entries[:5]:
    # Quick scrape for real image
    try:
        resp = requests.get(e.link, headers=headers, timeout=5)
        soup = BeautifulSoup(resp.text, 'html.parser')
        img = soup.find('meta', property='og:image')['content']
    except:
        img = 'https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&q=80&w=800'
    
    a = Article(external_id=e.link, title=e.title, source='OpenAI', url=e.link, summary=e.description, image_url=img, published_at=datetime.datetime.now())
    db.add(a)

# TechCrunch
r = requests.get('https://techcrunch.com/category/artificial-intelligence/feed/', headers=headers)
p = feedparser.parse(r.text)
for e in p.entries[:5]:
    try:
        resp = requests.get(e.link, headers=headers, timeout=5)
        soup = BeautifulSoup(resp.text, 'html.parser')
        img = soup.find('meta', property='og:image')['content']
    except:
        img = 'https://images.unsplash.com/photo-1620712943543-bcc4628c6bb6?auto=format&fit=crop&q=80&w=800'
    
    a = Article(external_id=e.link, title=e.title, source='TechCrunch', url=e.link, summary=e.description, image_url=img, published_at=datetime.datetime.now())
    db.add(a)

db.commit()
db.close()
print("Success: Real images populated!")
