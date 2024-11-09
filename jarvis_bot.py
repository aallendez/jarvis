import requests 
from flask import Flask, request, jsonify
from athletic_logger import reserve_swim, reserve_gym
import os

app = Flask(__name__)

# VERIFICATION_TOKEN = os.getenv('VERIFICATION_TOKEN')
# ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
# PHONE_NUMBER_ID = os.getenv('PHONE_NUMBER_ID')

VERIFICATION_TOKEN = "aZ7qL9sX3bNpRwT5"
ACCESS_TOKEN = 'EAAMSU02Fu7YBO60bfwnB8WgWf2iuQuklMLOq1bXTVSqBPQPeJXLxTZCUbRtTJBrqWiaDXf6h24SXkraQkMyokCjGHmRyni6IhtufBnBDoqWGd52hXm5X5LLVMG4RIqZBp6yiz8Wbmo58XCCHb6ZBuq7CW5affkXrHkGtZB2GAuru7B0aVXZBjgiFktZAAotTWwwczphQx02GBtBbe6maeQablCccYZD'
PHONE_NUMBER_ID = '512398011948890' 

API_URL = f'https://graph.facebook.com/v21.0/{PHONE_NUMBER_ID}/messages'

headers = {
    'Authorization': f'Bearer {ACCESS_TOKEN}',
    'Content-Type': 'application/json'
}

def send_whatsapp(to, template):
    data = {
        "messaging_product": "whatsapp",
        "to": to,  
        "type": "template",
        "template": {
            "name": template,  
            "language": {"code": "en"}
        }
    }

    response = requests.post(API_URL, headers=headers, json=data)
    print("API response status:", response.status_code)  # Print status code
    print("API response text:", response.text)  # Print response body

    if response.status_code == 200:
        print("Message sent successfully!")
    else:
        print("Failed to send message:", response.text)

        
@app.route('/')
def index():
    return "The app is running!", 200


@app.route('/train', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # Facebook's webhook verification
        token_sent = request.args.get("hub.verify_token")
        if token_sent == VERIFICATION_TOKEN:
            return request.args.get("hub.challenge")
        return "Verification token mismatch", 403
    
    # Existing POST handling code
    if request.method == 'POST':
        try:
            data = request.get_json()
            print("Received data:", data)  # Debug line to print incoming data

            message = data['messages'][0]['text']['body']
            sender_id = data['messages'][0]['from']
            print("Message:", message)  # Debug line to print message content
            print("Sender ID:", sender_id)  # Debug line to print sender ID

            time = 0

            if message.startswith("#train"):
                try:
                    # Split the message to extract the command parts
                    parts = message.split(" -")

                    # Check if we have enough parts for a valid command
                    if len(parts) >= 2:
                        # Extract sport
                        sport = parts[1].strip()
                        date = parts[2].strip() if len(parts) > 2 else None
                        print("Sport:", sport)  # Debug line
                        print("Date:", date)    # Debug line

                        if sport == "swim" and date:
                            send_whatsapp(sender_id, "gym_reservation_ack")
                            reserve_swim(date)
                        elif sport == "gym" and date:
                            send_whatsapp(sender_id, "gym_reservation_ack")
                            reserve_gym(date)
                        else:
                            send_whatsapp(sender_id, "gym_reservation_time_error" if date is None else "gym_reservation_format_error")
                    else:
                        send_whatsapp(sender_id, "gym_reservation_format_error")

                except ValueError as ve:
                    print("ValueError:", ve)  # Debug line for exceptions
                    send_whatsapp(sender_id, "automation_format_error")
                    return jsonify({"status": "error", "message": "Invalid command format"})

            return jsonify({"status": "received"}), 200
        
        except Exception as e:
            print("Exception:", e)  # General error logging
            return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)
    
    
