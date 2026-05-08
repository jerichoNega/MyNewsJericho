from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models
from database import SessionLocal, engine, get_db
from rss_parser import RSSParser
from summarizer import Summarizer
from messenger import Messenger
import yaml
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

load_dotenv()

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="MyNewsJericho AI API")

# CORS setup for React frontend
origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    os.getenv("FRONTEND_URL", "*")
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load config
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

rss_parser = RSSParser(config['feeds'])
summarizer = Summarizer(os.getenv("GEMINI_API_KEY"))
messenger = Messenger(
    os.getenv("TWILIO_ACCOUNT_SID"),
    os.getenv("TWILIO_AUTH_TOKEN"),
    os.getenv("TWILIO_WHATSAPP_NUMBER")
)

class ArticleSchema(BaseModel):
    id: int
    title: str
    source: str
    url: str
    summary: str
    ai_summary: Optional[str]
    image_url: Optional[str]
    category: str
    published_at: datetime
    is_bookmarked: bool

    class Config:
        from_attributes = True

@app.get("/")
def health_check():
    return {"status": "alive", "message": "MyNewsJericho AI Backend is running!"}

@app.get("/api/news", response_model=List[ArticleSchema])
def get_news(category: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(models.Article)
    if category and category != "All":
        query = query.filter(models.Article.category == category)
    articles = query.order_by(models.Article.published_at.desc()).all()
    return articles

@app.post("/api/fetch")
def fetch_news(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    def do_fetch():
        # We need a new session for the background task
        bg_db = SessionLocal()
        try:
            new_entries = rss_parser.fetch_new_entries_to_db(bg_db)
            print(f"Background Fetch: Found {len(new_entries)} new articles.")
            
            # Auto-notify WhatsApp for top 3 new articles
            if new_entries:
                user_num = os.getenv("USER_WHATSAPP_NUMBER")
                for entry in new_entries[:3]:
                    # Summarize if it doesn't have an AI summary
                    if not entry.ai_summary:
                        summary = summarizer.summarize({
                            'source': entry.source,
                            'title': entry.title,
                            'summary': entry.summary
                        })
                        entry.ai_summary = summary
                        bg_db.commit()
                    
                    msg = f"*New AI Insight*\n\n{entry.ai_summary}\n\nRead more: {entry.url}"
                    messenger.send_whatsapp_message(user_num, msg)
        finally:
            bg_db.close()

    background_tasks.add_task(do_fetch)
    return {"message": "Fetching news and sending WhatsApp notifications..."}

@app.post("/api/whatsapp/{article_id}")
def send_to_whatsapp(article_id: int, db: Session = Depends(get_db)):
    article = db.query(models.Article).filter(models.Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    # Generate summary if it doesn't exist
    if not article.ai_summary:
        article.ai_summary = summarizer.summarize({
            'source': article.source,
            'title': article.title,
            'summary': article.summary
        })
        db.commit()

    user_num = os.getenv("USER_WHATSAPP_NUMBER")
    msg = f"*AI Summary Request*\n\n{article.ai_summary}\n\nRead more: {article.url}"
    success = messenger.send_whatsapp_message(user_num, msg)
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to send WhatsApp message")
    
    return {"message": "Message sent to WhatsApp!"}

@app.post("/api/summarize/{article_id}")
def summarize_article(article_id: int, db: Session = Depends(get_db)):
    article = db.query(models.Article).filter(models.Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    if article.ai_summary:
        return {"summary": article.ai_summary}

    summary = summarizer.summarize({
        'source': article.source,
        'title': article.title,
        'summary': article.summary
    })
    
    article.ai_summary = summary
    db.commit()
    return {"summary": summary}

@app.patch("/api/bookmarks/{article_id}")
def toggle_bookmark(article_id: int, db: Session = Depends(get_db)):
    article = db.query(models.Article).filter(models.Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    article.is_bookmarked = not article.is_bookmarked
    db.commit()
    return {"is_bookmarked": article.is_bookmarked}

@app.get("/api/bookmarks", response_model=List[ArticleSchema])
def get_bookmarks(db: Session = Depends(get_db)):
    articles = db.query(models.Article).filter(models.Article.is_bookmarked == True).all()
    return articles

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
