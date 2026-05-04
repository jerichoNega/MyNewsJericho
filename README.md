# MyNewsJericho 📰

A "No-Code" feel Newsletter Aggregator WhatsApp bot that pulls daily news from RSS feeds, summarizes them using AI, and sends them directly to your phone.

## Features
- **RSS Ingestion:** Monitors multiple feeds (TechCrunch, The Verge, etc.).
- **AI Summarization:** Uses Google Gemini 1.5 Flash for concise, high-signal TL;DRs.
- **WhatsApp Delivery:** Sends summaries via Twilio's WhatsApp API.
- **State Management:** Tracks read articles to avoid duplicate messages.

## Setup

### 1. Prerequisites
- Python 3.8+
- A Twilio Account (for WhatsApp API)
- A Google AI Studio API Key (for Gemini)

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
   - `TWILIO_WHATSAPP_NUMBER` (Usually `whatsapp:+14155238886` for sandbox)
   - `GEMINI_API_KEY`
   - `USER_WHATSAPP_NUMBER` (Your phone number in `whatsapp:+1234567890` format)

3. Customize your feeds in `config.yaml`.

### 4. Running the Bot
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
This will run the bot every day at 9:00 AM.
