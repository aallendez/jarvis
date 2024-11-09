import requests 
from flask import Flask, request, jsonify
from athletic_logger import reserve_swim, reserve_gym

app = Flask(__name__)

# Define your access token and API endpoint
ACCESS_TOKEN = 'EAAMSU02Fu7YBO89US5vltH8GMZCkZBQkaXlIUpe1pFAxcLGLjhz0qZBbqWDfNxN20bBXsMKw66WqPteHZAXXBmDTrjZB7f3hnixy9ZAr8sXTuqqe8dRV9IZArtksGNHSwv8laBupIT7wrLBP6yQIj757a5iYmcwKyJqDv3UAN5FFQbpmWab7Be5nx6pG2tntd8T400pEmmZCMUslRtZB71IvzJy7Fi88ZD'
PHONE_NUMBER_ID = '512398011948890'  # Replace with your WhatsApp Business phone number ID
API_URL = f'https://graph.facebook.com/v21.0/{PHONE_NUMBER_ID}/messages'

headers = {
    'Authorization': f'Bearer {ACCESS_TOKEN}',
    'Content-Type': 'application/json'
}

def send_whatsapp(to, template):
    data = {
        "messaging_product": "whatsapp",
        "to": to,  # The recipient's WhatsApp number in international format
        "type": "template",
        "template": {
            "name": template,  # Replace with the actual name of your approved template
            "language": {"code": "en"}
        }
    }
    
    response = requests.post(API_URL, headers=headers, json=data)

    if response.status_code == 200:
        print("Message sent successfully!")
    else:
        print("Failed to send message:", response.text)

@app.route('/send-whatsapp', methods=['POST'])
def webhook():
    data = request.get_json()
    message = data['messages'][0]['text']['body']
    sender_id = data['messages'][0]['from']
    
    if message.startswith("#train"):
        send_whatsapp(sender_id, "gym_reservation_ack")
        
        try:
            command, sport = message.split(" -")
            if sport == "swim":
                command, day, time = command.split(" -")
                if day and time:
                    reserve_swim(day, time)
                else:
                    send_whatsapp(sender_id, "gym_reservation_time_error")
            elif sport == "gym":
                command, day, time = command.split(" -")
                if day and time:
                    reserve_gym(day, time)
                else:
                    send_whatsapp(sender_id, "gym_reservation_time_error")
            else:
                send_whatsapp(sender_id, "gym_reservation_format_error")
                
            
        except ValueError:
            send_whatsapp(sender_id, "automation_format_error")
            return jsonify({"status": "error", "message": "Invalid command format"})
    
    return jsonify({"status": "received"}), 200

if __name__ == '__main__':
    app.run(port=5000)