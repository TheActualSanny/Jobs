from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()

def send_sms(to_number, message_body):
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    twilio_phone_number = os.getenv('TWILIO_PHONE_NUMBER')

    if not account_sid or not auth_token or not twilio_phone_number:
        raise ValueError("Twilio credentials are not properly set in the environment variables")

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=message_body,
        from_=twilio_phone_number,
        to=to_number
    )
    
    return message.sid
