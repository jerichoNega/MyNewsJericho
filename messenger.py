from twilio.rest import Client
import os

class Messenger:
    def __init__(self, account_sid, auth_token, from_number):
        self.client = Client(account_sid, auth_token)
        self.from_number = from_number

    def send_whatsapp_message(self, to_number, message_body):
        print(f"Sending WhatsApp message...")
        print(f"DEBUG: From: '{self.from_number}'")
        print(f"DEBUG: To: '{to_number}'")
        try:
            message = self.client.messages.create(
                body=message_body,
                from_=self.from_number,
                to=to_number
            )
            print(f"Message sent! SID: {message.sid}")
            return True
        except Exception as e:
            print(f"Error sending WhatsApp message: {e}")
            return False
