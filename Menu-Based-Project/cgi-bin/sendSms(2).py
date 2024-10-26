#!/usr/bin/python3

import cgi
from twilio.rest import Client

# Print the content type header required for a CGI script
print("Content-Type: text/html")
print()

# Twilio account credentials
account_sid = ''
auth_token = ''
client = Client(account_sid, auth_token)

# Get the form data
form = cgi.FieldStorage()
sender_number = form.getvalue('phone')  # Updated to match HTML input name
message_body = form.getvalue('body')    # Updated to match HTML textarea name

try:
    # Create and send the SMS message using Twilio API
    message = client.messages.create(
        body=message_body,
        to=sender_number,
        from_=''  # Replace with your Twilio phone number
    )

    # Output a success message with the message SID
    print(f"<html><body><h1>Message Sent Successfully!</h1><p>Message SID: {message.sid}</p></body></html>")
except Exception as e:
    # Output an error message if the SMS could not be sent
    print(f"<html><body><h1>Error Sending Message</h1><p>{str(e)}</p></body></html>")

