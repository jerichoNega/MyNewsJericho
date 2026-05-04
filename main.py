import os
import yaml
import argparse
from dotenv import load_dotenv

from rss_parser import RSSParser
from state_manager import StateManager
from summarizer import Summarizer
from messenger import Messenger

def main():
    parser = argparse.ArgumentParser(description="MyNewsJericho: Newsletter Aggregator WhatsApp Bot")
    parser.add_argument("--dry-run", action="store_true", help="Run without sending WhatsApp messages or calling AI")
    parser.add_argument("--limit", type=int, default=5, help="Limit number of articles to process")
    args = parser.parse_args()

    # Load environment variables
    load_dotenv()
    
    # Load config
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)

    # Initialize components
    state_manager = StateManager()
    rss_parser = RSSParser(config['feeds'])
    
    # Check for new entries
    new_entries = rss_parser.fetch_new_entries(state_manager)
    
    if not new_entries:
        print("No new articles found.")
        return

    print(f"Found {len(new_entries)} new articles.")
    
    # Limit processing
    entries_to_process = new_entries[:args.limit]
    
    if args.dry_run:
        print("Dry run enabled. Summarizing first entry locally as an example...")
        entry = entries_to_process[0]
        print(f"--- DRY RUN ---\nSource: {entry['source']}\nTitle: {entry['title']}\n--- END DRY RUN ---")
        return

    # Initialize AI and Messenger
    gemini_key = os.getenv("GEMINI_API_KEY", "").strip()
    twilio_sid = os.getenv("TWILIO_ACCOUNT_SID", "").strip()
    twilio_token = os.getenv("TWILIO_AUTH_TOKEN", "").strip()
    twilio_from = os.getenv("TWILIO_WHATSAPP_NUMBER", "").strip()
    user_number = os.getenv("USER_WHATSAPP_NUMBER", "").strip()

    summarizer = Summarizer(gemini_key)
    messenger = Messenger(twilio_sid, twilio_token, twilio_from)

    for entry in entries_to_process:
        print(f"\n--- Processing: {entry['title']} ---")
        
        # 1. Summarize
        summary = summarizer.summarize(
            entry, 
            length=config['preferences'].get('summary_length', 'concise'),
            language=config['preferences'].get('language', 'English')
        )
        
        print(f"AI SUMMARY:\n{summary}\n")
        
        # 2. Format Message
        full_message = f"*Newsletter Summary*\n\n{summary}\n\nRead more: {entry['link']}"
        
        # 3. Send
        success = messenger.send_whatsapp_message(user_number, full_message)
        
        if success:
            state_manager.add_item(entry['id'])

    # Save state
    state_manager.save_state()
    print("All done!")

if __name__ == "__main__":
    main()
