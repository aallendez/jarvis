import requests

# Define your access token and API endpoint
ACCESS_TOKEN = 'EAAMSU02Fu7YBO89US5vltH8GMZCkZBQkaXlIUpe1pFAxcLGLjhz0qZBbqWDfNxN20bBXsMKw66WqPteHZAXXBmDTrjZB7f3hnixy9ZAr8sXTuqqe8dRV9IZArtksGNHSwv8laBupIT7wrLBP6yQIj757a5iYmcwKyJqDv3UAN5FFQbpmWab7Be5nx6pG2tntd8T400pEmmZCMUslRtZB71IvzJy7Fi88ZD'
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