from twilio.rest import Client

def send_sms(to_number, message_body):
    account_sid = ''
    auth_token = ''
    twilio_phone_number = ''

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=message_body,
        from_=twilio_phone_number,
        to=to_number
    )
    return message.sid
