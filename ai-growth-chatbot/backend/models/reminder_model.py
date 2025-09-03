from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb+srv://your-mongo-uri")
db = client["chatbot_db"]
reminders = db["reminders"]

def create_reminder(user_id, task, reminder_time):
    reminder = {
        "user_id": user_id,
        "task": task,
        "reminder_time": reminder_time,  # ISO datetime
        "status": "pending"
    }
    reminders.insert_one(reminder)
    return reminder
