import requests 
from flask import Flask, request, jsonify
from athletic_logger import reserve_swim, reserve_gym

import os

app = Flask(__name__)

VERIFICATION_TOKEN = os.getenv('VERIFICATION_TOKEN')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
PHONE_NUMBER_ID = os.getenv('PHONE_NUMBER_ID')

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
    
    # Handle POST request
    if request.method == 'POST':
        try:
            data = request.get_json()
            print("Received data:", data)  # Debug line to print incoming data

            # Access the message data safely
            entry = data.get("entry", [])[0]  # Get the first entry
            changes = entry.get("changes", [])[0]  # Get the first change
            message_value = changes.get("value", {})
            messages = message_value.get("messages", [])

            if not messages:
                print("No messages found in the received data.")
                return jsonify({"status": "error", "message": "No messages found"}), 400

            # Access message content
            message = messages[0]['text']['body']
            sender_id = messages[0]['from']
            print("Message:", message)  # Debug line to print message content
            print("Sender ID:", sender_id)  # Debug line to print sender ID

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
    
    
