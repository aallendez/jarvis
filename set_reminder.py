from send_whatsapp import send_whatsapp
from reminders_db import get_all_reminders, add_reminder
from flask import jsonify
from datetime import datetime, timedelta
import requests
import sqlite3

def set_reminder(message, sender_id):
    try:
        parts = message.split(" -")
        
        if len(parts) == 4:  # Expecting four parts after splitting
            day = parts[1].strip()
            time = parts[2].strip()
            reminder = parts[3].strip()
            
            # Convert 'today' and 'tomorrow' to actual dates
            if day == "today" or day == "Today":
                day = datetime.today().strftime("%d/%m/%Y")
            elif day == "tomorrow" or day == "Tomorrow":
                day = (datetime.today() + timedelta(days=1)).strftime("%d/%m/%Y")
            
            formatted_datetime = f"{day} at {time}"
            print(f"Day: {day}\nTime: {time}\nReminder: {reminder}")
            
            add_reminder(day, time, reminder, sender_id)
            
            send_whatsapp(sender_id, "reminder_ack", [reminder, formatted_datetime])
        
        elif message == "#remember -show":
            reminders = get_all_reminders(sender_id)  # Returns a single formatted string
            send_whatsapp(sender_id, "show_reminders", [reminders])
        else:
            send_whatsapp(sender_id, "command_format_error")
        
    except ValueError as ve:
        print("ValueError:", ve)  # Debug line for exceptions
        send_whatsapp(sender_id, "command_format_error")
        return jsonify({"status": "error", "message": "Invalid command format"})
    
