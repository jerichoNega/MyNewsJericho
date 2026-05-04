import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

sid = os.getenv('TWILIO_ACCOUNT_SID', '').strip()
token = os.getenv('TWILIO_AUTH_TOKEN', '').strip()

print(f"--- Debugging Twilio for SID: {sid} ---")

try:
    client = Client(sid, token)
    
    # Test 1: Check Account Access
    account = client.api.v2010.accounts(sid).fetch()
    print(f"✅ Connection successful! Account Name: {account.friendly_name}")
    print(f"Account Status: {account.status}")

    # Test 2: Check for active WhatsApp Sandbox
    print("\n--- Checking for WhatsApp Sandbox Number ---")
    # We'll try to send a test message to see what Twilio says
    try:
        # We use a dummy message to see if the FROM address is valid for this SID
        client.messages.create(
            from_='whatsapp:+14155238886',
            body='Internal Test',
            to='whatsapp:+31645112760'
        )
        print("✅ Message accepted by Twilio (Check your phone!)")
    except Exception as e:
        print(f"❌ Twilio rejected the number +14155238886.")
        print(f"Error Message: {e}")
        print("\nACTION NEEDED:")
        print("1. Go to: https://console.twilio.com/us1/develop/sms/settings/whatsapp-sandbox")
        print("2. Confirm the 'Sandbox Phone Number' listed there.")
        print("3. If it is NOT +1 415 523 8886, please tell me the correct one!")

except Exception as e:
    print(f"❌ Failed to connect to Twilio.")
    print(f"Error: {e}")
    print("Please double check your SID and Token in the .env file.")
