from send_whatsapp import send_whatsapp
from athletic_logger import reserve_swim, reserve_gym
from flask import jsonify

def athletic_reservation(message, sender_id):
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
    