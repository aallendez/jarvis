import datetime
import requests
import sqlite3
import threading
import time
from flask import Flask, request, jsonify
from reminders_db import get_all_reminders, init_db, check_and_send_reminders
from send_whatsapp import send_whatsapp
# from sport_reservation import athletic_reservation
from set_reminder import set_reminder
import os

app = Flask(__name__)

VERIFICATION_TOKEN = os.getenv('VERIFICATION_TOKEN')

# Initialize the database at startup
# init_db()

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

            # if message.startswith("#train"):
            #     athletic_reservation(message, sender_id)
            if message.startswith("#help"):
                send_whatsapp(message, sender_id)
            elif message.startswith("#log"):
                ...
            elif message.startswith("#remember"):
                set_reminder(message, sender_id)


            return jsonify({"status": "received"}), 200
        
        except Exception as e:
            print("Exception:", e)  # General error logging
            return jsonify({"status": "error", "message": str(e)}), 500

# Background function for checking reminders
def run_reminder_checker():
    while True:
        check_and_send_reminders()
        time.sleep(10) 

if __name__ == '__main__':
    # Start the reminder-checking thread
    reminder_thread = threading.Thread(target=run_reminder_checker, daemon=True)
    reminder_thread.start()

    # Run the Flask app
    app.run(port=5000, debug=True)
