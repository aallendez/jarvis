import requests

# Define your access token and API endpoint
ACCESS_TOKEN = 'EAAMSU02Fu7YBO60bfwnB8WgWf2iuQuklMLOq1bXTVSqBPQPeJXLxTZCUbRtTJBrqWiaDXf6h24SXkraQkMyokCjGHmRyni6IhtufBnBDoqWGd52hXm5X5LLVMG4RIqZBp6yiz8Wbmo58XCCHb6ZBuq7CW5affkXrHkGtZB2GAuru7B0aVXZBjgiFktZAAotTWwwczphQx02GBtBbe6maeQablCccYZD'
PHONE_NUMBER_ID = '512398011948890'  # Replace with your WhatsApp Business phone number ID
API_URL = f'https://graph.facebook.com/v21.0/{PHONE_NUMBER_ID}/messages'

headers = {
    'Authorization': f'Bearer {ACCESS_TOKEN}',
    'Content-Type': 'application/json'
}

def send_message(to, message_text):
    data = {
        "messaging_product": "whatsapp",
        "to": to,  # The recipient's WhatsApp number in international format
        "type": "template",
        "template": {
            "name": "gym_reservation_ack",  # Replace with the actual name of your approved template
            "language": {"code": "en"}
        }
    }

    response = requests.post(API_URL, headers=headers, json=data)

    if response.status_code == 200:
        print("Message sent successfully!")
    else:
        print("Failed to send message:", response.text)
        
m = "Hola Juan, soy Jarvis. ¡Tengo ganas de trabajar contigo!"
send_message("+34609140983", m)