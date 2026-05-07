import { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import { Bookmark, RefreshCw, Sparkles, ExternalLink, Bell, BellOff, X, Globe } from 'lucide-react';
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
  const [summarizingIds, setSummarizingIds] = useState<Record<number, boolean>>({});
  const [errorIds, setErrorIds] = useState<Record<number, string>>({});
  const [activeCategory, setActiveCategory] = useState('All');
  const [showBookmarks, setShowBookmarks] = useState(false);
  const [notificationsEnabled, setNotificationsEnabled] = useState(Notification.permission === 'granted');
  const [selectedArticle, setSelectedArticle] = useState<Article | null>(null);

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
    setSummarizingIds(prev => ({ ...prev, [id]: true }));
    setErrorIds(prev => ({ ...prev, [id]: '' }));
    try {
      const response = await axios.post(`${API_BASE_URL}/summarize/${id}`);
      const summary = response.data.summary;
      setArticles(prev => prev.map(a => a.id === id ? { ...a, ai_summary: summary } : a));
      if (selectedArticle?.id === id) {
        setSelectedArticle(prev => prev ? { ...prev, ai_summary: summary } : null);
      }
    } catch (error) {
      console.error('Error summarizing:', error);
      setErrorIds(prev => ({ ...prev, [id]: 'Failed to generate summary. Try again.' }));
    } finally {
      setSummarizingIds(prev => ({ ...prev, [id]: false }));
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

  const openPreview = (article: Article) => {
    setSelectedArticle(article);
    if (!article.ai_summary) {
      handleSummarize(article.id);
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
              <div key={article.id} className="news-card" onClick={() => openPreview(article)}>
                <div className="card-image">
                  <img 
                    src={article.image_url || 'https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&q=80&w=800'} 
                    alt={article.title} 
                    loading="lazy"
                    referrerPolicy="no-referrer"
                    onError={(e) => {
                      e.currentTarget.src = 'https://images.unsplash.com/photo-1485827404703-89b55fcc595e?auto=format&fit=crop&q=80&w=800';
                    }} 
                  />
                </div>
                <div className="card-content">
                  <div className="card-header">
                    <span className="source">{article.source}</span>
                    <span className="date">{new Date(article.published_at).toLocaleDateString()}</span>
                  </div>
                  <h3>{article.title}</h3>
                  <p className="summary" dangerouslySetInnerHTML={{ __html: article.summary }}></p>
                  
                  {summarizingIds[article.id] ? (
                    <div className="ai-summary loading-pulse">
                      <p>AI is thinking...</p>
                    </div>
                  ) : errorIds[article.id] ? (
                    <div className="ai-summary error">
                      <p>{errorIds[article.id]}</p>
                    </div>
                  ) : article.ai_summary ? (
                    <div className="ai-summary">
                      <h4><Sparkles size={14} /> AI Summary</h4>
                      <p>{article.ai_summary}</p>
                    </div>
                  ) : null}
                  <div className="card-footer">
                    <span className="link">
                      Quick Preview <ExternalLink size={14} />
                    </span>
                    <div className="actions">
                      <button onClick={(e) => { e.stopPropagation(); handleSummarize(article.id); }} title="AI Summarize">
                        <Sparkles size={18} color={article.ai_summary ? '#6366f1' : '#64748b'} />
                      </button>
                      <button onClick={(e) => { e.stopPropagation(); toggleBookmark(article.id); }} title="Bookmark">
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

      {/* Smart Preview Drawer */}
      {selectedArticle && (
        <div className="drawer-overlay" onClick={() => setSelectedArticle(null)}>
          <div className="drawer" onClick={(e) => e.stopPropagation()}>
            <div className="drawer-header">
              <div className="title-area">
                <span className="source">{selectedArticle.source}</span>
                <h2>{selectedArticle.title}</h2>
              </div>
              <button className="close-btn" onClick={() => setSelectedArticle(null)}>
                <X size={20} />
              </button>
            </div>
            <div className="drawer-content">
              <div className="preview-smart-box">
                <h3><Sparkles size={18} /> The Core Concept</h3>
                {summarizingIds[selectedArticle.id] ? (
                  <p className="loading-pulse">Analyzing the article's core intent...</p>
                ) : selectedArticle.ai_summary ? (
                  <p>{selectedArticle.ai_summary}</p>
                ) : (
                  <p>Initializing AI analysis...</p>
                )}
              </div>
              
              <div className="iframe-container">
                <div className="iframe-header" style={{ padding: '0.5rem', background: '#f1f5f9', fontSize: '0.8rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <Globe size={12} /> {selectedArticle.url}
                </div>
                <iframe 
                  src={selectedArticle.url} 
                  title="Source Preview"
                  sandbox="allow-same-origin allow-scripts"
                />
                <div className="iframe-fallback">
                  <p>Site prevented direct preview. Use the button below to visit the full article.</p>
                </div>
              </div>
            </div>
            <div className="drawer-footer">
              <a href={selectedArticle.url} target="_blank" rel="noopener noreferrer" className="btn-primary">
                Visit Full Website <ExternalLink size={18} />
              </a>
              <button 
                onClick={() => toggleBookmark(selectedArticle.id)} 
                className={`btn-secondary ${selectedArticle.is_bookmarked ? 'active' : ''}`}
                style={{ flexGrow: 0 }}
              >
                <Bookmark size={20} fill={selectedArticle.is_bookmarked ? '#6366f1' : 'none'} />
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
