import datetime
import requests
import sqlite3
import time
from send_whatsapp import send_whatsapp

# Initialize the SQLite database and create a reminders table if it doesn’t exist
def init_db():
    conn = sqlite3.connect('reminders.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS reminders (
                    id INTEGER PRIMARY KEY,
                    date TEXT,
                    time TEXT,
                    reminder TEXT,
                    sender_id TEXT
                 )''')
    conn.commit()
    conn.close()

# Function to add a new reminder
def add_reminder(date, time, reminder, sender_id):
    conn = sqlite3.connect('reminders.db')
    c = conn.cursor()
    c.execute("INSERT INTO reminders (date, time, reminder, sender_id) VALUES (?, ?, ?, ?)", 
              (date, time, reminder, sender_id))
    conn.commit()
    conn.close()

# Function to fetch and delete reminders that are due
def check_and_send_reminders():
    conn = sqlite3.connect('reminders.db')
    c = conn.cursor()
    now = datetime.datetime.now()
    reminders_to_send = []

    for row in c.execute("SELECT * FROM reminders"):
        reminder_time = datetime.datetime.strptime(row[1] + " " + row[2], "%d/%m/%Y %H:%M")
        if now >= reminder_time:
            reminders_to_send.append(row)
    
    # Send reminders and delete them after sending
    for reminder in reminders_to_send:
        reminder_text = reminder[3]  # The reminder message text
        sender_id = reminder[4]      # The recipient's ID

        # Send the reminder using the "reminder_message" template
        send_whatsapp(sender_id, "reminder_message", [reminder_text])
        
        print(f"Sent reminder: {reminder_text} to {sender_id}")
        # Delete the reminder after sending
        c.execute("DELETE FROM reminders WHERE id = ?", (reminder[0],))

    conn.commit()
    conn.close()

def get_all_reminders(sender_id):
    conn = sqlite3.connect('reminders.db')
    c = conn.cursor()
    
    # Fetch all reminders from the database
    c.execute("SELECT date, time, reminder FROM reminders ORDER BY date, time")
    reminders = c.fetchall()
    conn.close()
    
    if not reminders:
        print("No reminders found for the user.")
        send_whatsapp(sender_id, "no_reminders_to_show")
        return None  # Return None if there are no reminders
    else:   
        print("Reminders found:", reminders)
        # Process reminders into a sorted, readable format
        reminder_strings = []
        for index, (date, time, reminder) in enumerate(reminders, start=1):
            # Format dates: check if today or day of the week, otherwise use dd/mm/yyyy
            reminder_date = datetime.datetime.strptime(date, "%d/%m/%Y").date()
            today = datetime.date.today()
            
            if reminder_date == today:
                date_str = "today"
            elif reminder_date == today + datetime.timedelta(days=1):
                date_str = "tomorrow"
            elif reminder_date < today + datetime.timedelta(days=7):
                date_str = reminder_date.strftime("%A")  # Day of the week
            else:
                date_str = reminder_date.strftime("%d/%m/%Y")  # Full date
            
            reminder_strings.append(f"{index}. {reminder}, {date_str}, {time}")
    
    # Join all reminders into a single formatted string
    return "\n".join(reminder_strings)


