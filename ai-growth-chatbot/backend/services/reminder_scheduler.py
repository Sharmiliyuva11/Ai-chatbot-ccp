from apscheduler.schedulers.background import BackgroundScheduler
from pymongo import MongoClient
from datetime import datetime
from email_service import email_service
import pytz
import os

# MongoDB setup
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
DB_NAME = os.getenv('MONGO_DB', 'coby_db')
REMINDERS_COLLECTION = os.getenv('REMINDERS_COLLECTION', 'reminders')
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
reminders_col = db[REMINDERS_COLLECTION]

# APScheduler setup
scheduler = BackgroundScheduler()

# Helper: parse reminder datetime

def get_reminder_datetime(reminder):
    tz = pytz.timezone(reminder.get('timezone', 'UTC'))
    date_str = reminder.get('date')
    time_str = reminder.get('time')
    if not date_str or not time_str:
        return None
    dt_str = f"{date_str} {time_str}"
    try:
        dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
        return tz.localize(dt)
    except Exception:
        return None

# Job: send reminder email

def send_reminder_job(reminder_id):
    reminder = reminders_col.find_one({'_id': reminder_id})
    if not reminder:
        return
    to_email = reminder.get('user_email')
    if to_email:
        email_service.send_reminder_email(to_email, reminder)

# Scheduler: scan DB and schedule jobs

def schedule_reminders():
    now = datetime.utcnow().replace(tzinfo=pytz.UTC)
    upcoming = reminders_col.find({
        'notified': {'$ne': True},
        'date': {'$exists': True},
        'time': {'$exists': True}
    })
    for reminder in upcoming:
        reminder_dt = get_reminder_datetime(reminder)
        if not reminder_dt:
            continue
        # Only schedule if in the future
        if reminder_dt > now:
            job_id = f"reminder_{str(reminder['_id'])}"
            if not scheduler.get_job(job_id):
                scheduler.add_job(
                    send_reminder_job,
                    'date',
                    run_date=reminder_dt,
                    args=[reminder['_id']],
                    id=job_id
                )

# Mark reminders as notified after sending (optional, can be done in send_reminder_job)

# Flask integration example

def start_scheduler():
    scheduler.start()
    schedule_reminders()

# Call start_scheduler() when your Flask app starts (e.g. in app.py)

# Example: in app.py
# from services.reminder_scheduler import start_scheduler
# start_scheduler()

# To rescan and schedule new reminders, you can call schedule_reminders() periodically (e.g. every minute)
# Example: scheduler.add_job(schedule_reminders, 'interval', minutes=1)

# Make sure reminders in MongoDB have fields: _id, user_email, title, description, date (YYYY-MM-DD), time (HH:MM), timezone (optional)
