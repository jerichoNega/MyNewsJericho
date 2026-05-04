# MyNewsJericho 📰

A streamlined Newsletter Aggregator and WhatsApp Messenger that pulls daily news from RSS feeds, processes them into high-signal summaries, and sends them directly to your phone.

## Features
- **RSS Ingestion:** Monitors multiple feeds (TechCrunch, The Verge, etc.).
- **Smart Processing:** Uses custom engines for concise, high-signal TL;DRs.
- **WhatsApp Delivery:** Sends updates via WhatsApp.
- **State Management:** Tracks read articles to avoid duplicate messages.

## Setup

### 1. Prerequisites
- Python 3.8+
- A Twilio Account (for WhatsApp)
- A processing engine API key

### 2. Installation
```bash
git clone <this-repo>
cd MyNewsJericho
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configuration
1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Fill in your credentials in `.env`:
   - `TWILIO_ACCOUNT_SID`
   - `TWILIO_AUTH_TOKEN`
   - `TWILIO_WHATSAPP_NUMBER`
   - `GEMINI_API_KEY` (Processing Engine Key)
   - `USER_WHATSAPP_NUMBER` (Your phone number)

3. Customize your feeds in `config.yaml`.

### 4. Running the System
**Dry Run (Test only):**
```bash
python main.py --dry-run
```

**Live Run (Sends messages):**
```bash
python main.py
```

## Automation
To run this daily, you can set up a cron job:
```bash
0 9 * * * /path/to/MyNewsJericho/venv/bin/python /path/to/MyNewsJericho/main.py
```
This will run the system every day at 9:00 AM.
