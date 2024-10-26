#!/usr/bin/env python3
import cgi
import cgitb
from twilio.rest import Client
import json

# Enable error reporting
cgitb.enable()
print("Content-Type: text/html\n")

# Twilio configuration
TWILIO_ACCOUNT_SID = ''
TWILIO_AUTH_TOKEN = ''
TWILIO_WHATSAPP_NUMBER = ''

def send_whatsapp_message(to, message):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=message,
        from_=TWILIO_WHATSAPP_NUMBER,
        to=f'whatsapp:{to}'
    )
    return message.sid

form = cgi.FieldStorage()
phone = form.getvalue('phone')
body = form.getvalue('body')

if phone and body:
    try:
        message_sid = send_whatsapp_message(phone, body)
        print(f'Message sent successfully! Message SID: {message_sid}')
    except Exception as e:
        print(f'Error: {str(e)}')
else:
    print('Error: Missing phone number or message body.')