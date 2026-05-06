# Deployment Guide

Follow these 3 simple steps to put your AI News System online.

---

### Step 1: Upload your code to GitHub
If you haven't already, create a new repository on GitHub and run these commands in your project folder:
1. `git add .`
2. `git commit -m "ready for deploy"`
3. `git remote add origin YOUR_GITHUB_REPO_URL`
4. `git push -u origin main`

---

### Step 2: Deploy the Backend (on Render.com)
1. Go to [Render.com](https://dashboard.render.com/) and Log in with GitHub.
2. Click **New +** > **Blueprint**.
3. Select your repository.
4. It will automatically detect the settings from `render.yaml`.
5. When it asks for **GEMINI_API_KEY**, paste your key.
6. Click **Apply**. 
7. Once finished, copy the "Service URL" (e.g., `https://ai-news-backend.onrender.com`).

---

### Step 3: Deploy the Frontend (on Netlify.com)
1. Go to [Netlify.com](https://app.netlify.com/) and Log in with GitHub.
2. Click **Add new site** > **Import from GitHub**.
3. Select your repository.
4. Netlify will automatically see the `netlify.toml` and configure everything.
5. **Crucial**: Go to **Site Settings** > **Environment Variables**.
6. Click **Add Variable**:
   - Key: `VITE_API_URL`
   - Value: `YOUR_RENDER_URL/api` (the one you copied in Step 2).
7. Click **Deploy**.

---

**You're done! Your site is live.**
