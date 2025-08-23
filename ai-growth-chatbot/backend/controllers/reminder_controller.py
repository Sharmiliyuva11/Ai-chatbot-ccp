from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv
from services.email_service import email_service  # <-- for sending email

load_dotenv()

# MongoDB connection
try:
    mongo_uri = os.getenv("MONGO_URI")
    if mongo_uri and mongo_uri != "mongodb+srv://<username>:<password>@cluster0.mongodb.net/?retryWrites=true&w=majority":
        client = MongoClient(mongo_uri)
        db = client.get_database("ai_chatbot_ccp")
        reminders_collection = db["reminders"]
    else:
        print("Warning: Using in-memory storage for reminders. Set MONGO_URI in .env for persistent storage.")
        reminders_collection = None
except Exception as e:
    print(f"MongoDB connection failed: {e}")
    print("Using in-memory storage for reminders.")
    reminders_collection = None

# In-memory storage for testing
_reminders_memory = []

# Blueprint
reminder_bp = Blueprint('reminder', __name__)

# Add a reminder
@reminder_bp.route('/', methods=['POST'])
@jwt_required()
def add_reminder():
    user_id = get_jwt_identity()
    data = request.get_json()
    title = data.get("title")
    description = data.get("description")
    remind_at_str = data.get("remind_at")  # e.g. "2025-08-08 10:00:00"
    email = data.get("email")  # Optional: send to user

    if not (title and description and remind_at_str):
        return jsonify({"success": False, "message": "All fields are required."}), 400

    try:
        remind_at = datetime.strptime(remind_at_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return jsonify({"success": False, "message": "Invalid datetime format. Use YYYY-MM-DD HH:MM:SS"}), 400

    try:
        reminder = {
            "user_id": user_id,
            "title": title,
            "description": description,
            "remind_at": remind_at,
            "created_at": datetime.utcnow()
        }
        
        if reminders_collection is not None:
            reminders_collection.insert_one(reminder)
        else:
            # In-memory storage
            reminder["_id"] = len(_reminders_memory) + 1
            _reminders_memory.append(reminder)

        # Optional: Send immediate email confirmation
        if email:
            try:
                email_service.send_email(
                    to_email=email,
                    subject=f"🧠 New Reminder Set: {title}",
                    body=f"You've set a new reminder:\n\n{description}\n\nRemind At: {remind_at_str}"
                )
            except Exception as email_error:
                print(f"Email sending failed: {email_error}")

        return jsonify({"success": True, "message": "Reminder added successfully."}), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# Get all reminders for logged-in user
@reminder_bp.route('/', methods=['GET'])
@jwt_required()
def get_reminders():
    user_id = get_jwt_identity()
    try:
        if reminders_collection is not None:
            reminders = list(reminders_collection.find({"user_id": user_id}))
            for r in reminders:
                r["_id"] = str(r["_id"])
                r["remind_at"] = r["remind_at"].strftime("%Y-%m-%d %H:%M:%S")
                r["created_at"] = r["created_at"].strftime("%Y-%m-%d %H:%M:%S")
        else:
            # In-memory storage
            reminders = []
            for r in _reminders_memory:
                if r["user_id"] == user_id:
                    reminder_copy = r.copy()
                    reminder_copy["_id"] = str(reminder_copy["_id"])
                    reminder_copy["remind_at"] = reminder_copy["remind_at"].strftime("%Y-%m-%d %H:%M:%S")
                    reminder_copy["created_at"] = reminder_copy["created_at"].strftime("%Y-%m-%d %H:%M:%S")
                    reminders.append(reminder_copy)
        
        return jsonify({"success": True, "reminders": reminders})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# Delete a reminder
@reminder_bp.route('/<reminder_id>', methods=['DELETE'])
@jwt_required()
def delete_reminder(reminder_id):
    user_id = get_jwt_identity()
    try:
        if reminders_collection is not None:
            from bson.objectid import ObjectId
            result = reminders_collection.delete_one({
                "_id": ObjectId(reminder_id),
                "user_id": user_id
            })
            if result.deleted_count == 0:
                return jsonify({"success": False, "message": "Reminder not found."}), 404
        else:
            # In-memory storage
            found = False
            for i, r in enumerate(_reminders_memory):
                if str(r["_id"]) == reminder_id and r["user_id"] == user_id:
                    _reminders_memory.pop(i)
                    found = True
                    break
            if not found:
                return jsonify({"success": False, "message": "Reminder not found."}), 404
        
        return jsonify({"success": True, "message": "Reminder deleted."})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
