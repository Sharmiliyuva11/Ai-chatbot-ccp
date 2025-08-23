from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# MongoDB setup
client = MongoClient(os.getenv("MONGO_URI"))
db = client.get_database("ai_chatbot_ccp")
chat_collection = db["chats"]

class ChatModel:
    @staticmethod
    def save_message(user_id, user_input, bot_response):
        chat_document = {
            "user_id": user_id,
            "user_input": user_input,
            "bot_response": bot_response,
            "timestamp": datetime.utcnow()
        }
        chat_collection.insert_one(chat_document)

    @staticmethod
    def get_user_chats(user_id, limit=20):
        chats = chat_collection.find({"user_id": user_id}).sort("timestamp", -1).limit(limit)
        return [{
            "_id": str(chat["_id"]),
            "user_input": chat["user_input"],
            "bot_response": chat["bot_response"],
            "timestamp": chat["timestamp"]
        } for chat in chats]
