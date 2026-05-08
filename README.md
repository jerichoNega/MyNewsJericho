# MyNewsJericho AI

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/jerichoNega/MyNewsJericho)
[![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start/deploy?repository=https://github.com/jerichoNega/MyNewsJericho)

MyNewsJericho AI is a high-performance, full-stack news aggregation and analysis dashboard designed specifically for the AI ecosystem. It provides an immersive, visual command center for tracking the latest breakthroughs, research papers, and industry trends from world-class sources.

## ✨ Core Features

*   **Elite Source Aggregation**: Real-time tracking of OpenAI, Google AI, TechCrunch AI, VentureBeat, arXiv (cs.AI), and HackerNews.
*   **Intelligent Summarization**: Integrated AI-powered content synthesis that extracts the "Core Concept" from long-form articles and research papers.
*   **Immersive Smart Preview**: A sophisticated side-panel preview system with spring-style animations, allowing users to analyze articles and glimpse source websites without leaving the feed.
*   **Visual-First Dashboard**: Deep image scraping that captures featured thumbnails from article OpenGraph data for a professional, media-rich experience.
*   **Real-time Notifications**: Browser-level notification system that alerts you the moment groundbreaking AI news is indexed.
*   **Smart Filtering & Bookmarking**: Categorized views (Development, Trends, Research, Tech) and a persistent bookmarking system for deep study.

## 🛠️ Technical Architecture

### Backend (Python/FastAPI)
- **FastAPI**: High-concurrency REST API.
- **SQLAlchemy + SQLite**: Robust data persistence and caching.
- **Feedparser & BeautifulSoup4**: Advanced RSS aggregation and deep OpenGraph image scraping.
- **Gemini Pro API**: Large Language Model integration for intelligent summarization.

### Frontend (React/TypeScript)
- **React 19 + Vite**: Modern, ultra-fast frontend performance.
- **Lucide React**: Clean, consistent iconography.
- **Axios**: Sophisticated API state management with polling and loading handlers.
- **CSS3 Animations**: Custom cubic-bezier spring animations and responsive grid layouts.

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- Google Gemini API Key

### Installation

1. **Clone and Setup Backend**:
   ```bash
   cd MyNewsJericho
   python -m venv venv
   source venv/bin/activate  # venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

2. **Configure Environment**:
   Create a `.env` file in the root:
   ```env
   GEMINI_API_KEY=your_key_here
   ```

3. **Setup Frontend**:
   ```bash
   cd frontend
   npm install
   ```

4. **Run the System**:
   - Backend: `uvicorn api:app --reload`
   - Frontend: `npm run dev`

## 🌐 Deployment

The system is configured for split-deployment:
- **Backend**: Ready for Render or Heroku (Procfile and `render.yaml` included).
- **Frontend**: Ready for Netlify or Vercel (`netlify.toml` included).

## 📝 License

MIT
