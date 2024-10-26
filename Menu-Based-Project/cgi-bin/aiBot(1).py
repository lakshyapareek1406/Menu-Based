#!/usr/bin/python3

import cgi
import os
import google.generativeai as genai

print("Content-Type: text/plain\n")

# Configure the API key
genai.configure(api_key="")

# Define the generation configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Create the generative model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# Start a chat session
chat_session = model.start_chat(history=[])

# Parse form data
form = cgi.FieldStorage()
prompt = form.getvalue('prompt')

# Send the prompt to the model and get the response
response = chat_session.send_message(prompt)
print(response.text)