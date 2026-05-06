import { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import { Bookmark, RefreshCw, Sparkles, ExternalLink, Bell, BellOff } from 'lucide-react';
import './App.css';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

interface Article {
  id: number;
  title: string;
  source: string;
  url: string;
  summary: string;
  ai_summary?: string;
  image_url?: string;
  category: string;
  published_at: string;
  is_bookmarked: boolean;
}

function App() {
  const [articles, setArticles] = useState<Article[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeCategory, setActiveCategory] = useState('All');
  const [showBookmarks, setShowBookmarks] = useState(false);
  const [notificationsEnabled, setNotificationsEnabled] = useState(Notification.permission === 'granted');

  const categories = ['All', 'AI Development', 'Trends', 'Research', 'General Tech'];

  const fetchNews = useCallback(async (isInitial = false) => {
    if (isInitial) setLoading(true);
    try {
      const endpoint = showBookmarks ? '/bookmarks' : `/news?category=${activeCategory}`;
      const response = await axios.get(`${API_BASE_URL}${endpoint}`);
      
      // If we have new articles and notifications are on, notify!
      if (!isInitial && !showBookmarks && response.data.length > articles.length && articles.length > 0) {
        const newOnes = response.data.filter((a: Article) => !articles.find(existing => existing.id === a.id));
        if (newOnes.length > 0 && notificationsEnabled) {
          new Notification('New AI Insights!', {
            body: newOnes[0].title,
            icon: '/favicon.svg'
          });
        }
      }
      
      setArticles(response.data);
    } catch (error) {
      console.error('Error fetching news:', error);
    } finally {
      if (isInitial) setLoading(false);
    }
  }, [activeCategory, showBookmarks, articles, notificationsEnabled]);

  useEffect(() => {
    fetchNews(true);
  }, [activeCategory, showBookmarks]);

  // Poll for updates every 2 minutes
  useEffect(() => {
    const interval = setInterval(() => fetchNews(false), 120000);
    return () => clearInterval(interval);
  }, [fetchNews]);

  const requestNotificationPermission = async () => {
    const permission = await Notification.requestPermission();
    setNotificationsEnabled(permission === 'granted');
  };

  const handleFetch = async () => {
    try {
      await axios.post(`${API_BASE_URL}/fetch`);
      alert('Fetching new articles in background...');
    } catch (error) {
      console.error('Error triggering fetch:', error);
    }
  };

  const handleSummarize = async (id: number) => {
    try {
      const response = await axios.post(`${API_BASE_URL}/summarize/${id}`);
      setArticles(articles.map(a => a.id === id ? { ...a, ai_summary: response.data.summary } : a));
    } catch (error) {
      console.error('Error summarizing:', error);
    }
  };

  const toggleBookmark = async (id: number) => {
    try {
      const response = await axios.patch(`${API_BASE_URL}/bookmarks/${id}`);
      const updatedStatus = response.data.is_bookmarked;
      
      if (showBookmarks && !updatedStatus) {
        setArticles(articles.filter(a => a.id !== id));
      } else {
        setArticles(articles.map(a => a.id === id ? { ...a, is_bookmarked: updatedStatus } : a));
      }
    } catch (error) {
      console.error('Error toggling bookmark:', error);
    }
  };

  return (
    <div className="app-container">
      <header>
        <div className="logo">
          <Sparkles className="icon-sparkle" />
          <h1>MyNewsJericho AI</h1>
        </div>
        <div className="header-actions">
          <button 
            onClick={requestNotificationPermission} 
            className={`btn-icon ${notificationsEnabled ? 'enabled' : ''}`}
            title={notificationsEnabled ? 'Notifications On' : 'Enable Notifications'}
          >
            {notificationsEnabled ? <Bell size={20} /> : <BellOff size={20} />}
          </button>
          <button onClick={handleFetch} className="btn-secondary">
            <RefreshCw size={18} />
            Fetch New
          </button>
          <button 
            onClick={() => setShowBookmarks(!showBookmarks)} 
            className={`btn-secondary ${showBookmarks ? 'active' : ''}`}
          >
            <Bookmark size={18} />
            Bookmarks
          </button>
        </div>
      </header>

      {!showBookmarks && (
        <nav className="filter-bar">
          {categories.map(cat => (
            <button 
              key={cat} 
              className={activeCategory === cat ? 'active' : ''}
              onClick={() => setActiveCategory(cat)}
            >
              {cat}
            </button>
          ))}
        </nav>
      )}

      {showBookmarks && <h2 className="section-title">Saved Articles</h2>}

      <main>
        {loading ? (
          <div className="loading">Loading news...</div>
        ) : articles.length === 0 ? (
          <div className="loading">No articles found. Use "Fetch New" to pull content.</div>
        ) : (
          <div className="news-grid">
            {articles.map(article => (
              <div key={article.id} className="news-card">
                {article.image_url && (
                  <div className="card-image">
                    <img src={article.image_url} alt={article.title} loading="lazy" onError={(e) => (e.currentTarget.style.display = 'none')} />
                  </div>
                )}
                <div className="card-content">
                  <div className="card-header">
                    <span className="source">{article.source}</span>
                    <span className="date">{new Date(article.published_at).toLocaleDateString()}</span>
                  </div>
                  <h3>{article.title}</h3>
                  <p className="summary" dangerouslySetInnerHTML={{ __html: article.summary }}></p>
                  
                  {article.ai_summary && (
                    <div className="ai-summary">
                      <h4><Sparkles size={14} /> AI Summary</h4>
                      <p>{article.ai_summary}</p>
                    </div>
                  )}

                  <div className="card-footer">
                    <a href={article.url} target="_blank" rel="noopener noreferrer" className="link">
                      Read More <ExternalLink size={14} />
                    </a>
                    <div className="actions">
                      <button onClick={() => handleSummarize(article.id)} title="AI Summarize">
                        <Sparkles size={18} color={article.ai_summary ? '#6366f1' : '#64748b'} />
                      </button>
                      <button onClick={() => toggleBookmark(article.id)} title="Bookmark">
                        <Bookmark size={18} fill={article.is_bookmarked ? '#6366f1' : 'none'} color={article.is_bookmarked ? '#6366f1' : '#64748b'} />
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
