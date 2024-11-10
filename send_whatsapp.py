import os
import datetime
import requests
import sqlite3

ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
PHONE_NUMBER_ID = os.getenv('PHONE_NUMBER_ID')
API_URL = f'https://graph.facebook.com/v21.0/{PHONE_NUMBER_ID}/messages'

headers = {
    'Authorization': f'Bearer {ACCESS_TOKEN}',
    'Content-Type': 'application/json'
}

def send_whatsapp(to, template, variables=None):
    # Ensure variables are properly formatted as a list of dictionaries with 'text'
    components = [
        {
            "type": "body",
            "parameters": [{"type": "text", "text": var} for var in variables]
        }
    ] if variables else []

    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "template",
        "template": {
            "name": template,
            "language": {"code": "en"},
            "components": components
        }
    }

    response = requests.post(API_URL, headers=headers, json=data)
    print("API response status:", response.status_code)
    print("API response text:", response.text)

    if response.status_code == 200:
        print("Message sent successfully!")
    else:
        print("Failed to send message:", response.text)
