from pymongo import MongoClient
from bson import ObjectId
import os
import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB setup
try:
    mongo_uri = os.getenv("MONGO_URI")
    if mongo_uri and mongo_uri != "mongodb+srv://<username>:<password>@cluster0.mongodb.net/?retryWrites=true&w=majority":
        try:
            client = MongoClient(
                mongo_uri,
                tls=True,
                tlsAllowInvalidCertificates=True,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=10000,
                socketTimeoutMS=10000
            )
            client.admin.command('ping')
            db = client.get_database("ai_chatbot_ccp")
            sessions_collection = db["roundtable_sessions"]
            print("✅ Connected to MongoDB successfully with SSL for roundtable sessions")
        except Exception as ssl_error:
            print(f"⚠️ SSL connection failed: {ssl_error}")
            print("⚠️ Trying without SSL...")
            client = MongoClient(
                mongo_uri,
                tls=False,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=10000,
                socketTimeoutMS=10000
            )
            client.admin.command('ping')
            db = client.get_database("ai_chatbot_ccp")
            sessions_collection = db["roundtable_sessions"]
            print("✅ Connected to MongoDB successfully without SSL for roundtable sessions")
    else:
        print("⚠️ Warning: Using in-memory storage for roundtable sessions. Set MONGO_URI in .env for persistent storage.")
        sessions_collection = None
except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")
    print("⚠️ Using in-memory storage for roundtable sessions.")
    sessions_collection = None

# In-memory storage for testing
_sessions_memory = []

class RoundtableSession:
    @staticmethod
    def get_all_sessions():
        """Get all sessions for all users"""
        if sessions_collection is not None:
            return list(sessions_collection.find({}))
        else:
            return _sessions_memory.copy()

    @staticmethod
    def get_sessions_by_user(user_id):
        """Get sessions hosted by or joined by a user"""
        if sessions_collection is not None:
            return list(sessions_collection.find({
                "$or": [
                    {"host_id": user_id},
                    {"participants": user_id}
                ]
            }))
        else:
            return [s for s in _sessions_memory if s.get('host_id') == user_id or user_id in s.get('participants', [])]

    @staticmethod
    def find_by_id(session_id):
        """Find session by ID"""
        if sessions_collection is not None:
            try:
                return sessions_collection.find_one({"_id": ObjectId(session_id)})
            except:
                return None
        else:
            for session in _sessions_memory:
                if str(session.get('_id')) == str(session_id):
                    return session
            return None

    @staticmethod
    def create_session(session_data):
        """Create a new session"""
        session_data['created_at'] = datetime.datetime.utcnow()
        session_data['updated_at'] = datetime.datetime.utcnow()

        if sessions_collection is not None:
            result = sessions_collection.insert_one(session_data)
            session_data['_id'] = result.inserted_id
            return session_data
        else:
            session_id = len(_sessions_memory) + 1
            session_data['_id'] = session_id
            _sessions_memory.append(session_data)
            return session_data

    @staticmethod
    def update_session(session_id, update_data):
        """Update session data"""
        update_data['updated_at'] = datetime.datetime.utcnow()

        if sessions_collection is not None:
            try:
                result = sessions_collection.update_one(
                    {"_id": ObjectId(session_id)},
                    {"$set": update_data}
                )
                return result.modified_count > 0
            except:
                return False
        else:
            for i, session in enumerate(_sessions_memory):
                if str(session.get('_id')) == str(session_id):
                    _sessions_memory[i].update(update_data)
                    return True
            return False

    @staticmethod
    def join_session(session_id, user_id):
        """Add user to session participants"""
        if sessions_collection is not None:
            try:
                result = sessions_collection.update_one(
                    {"_id": ObjectId(session_id)},
                    {
                        "$addToSet": {"participants": user_id},
                        "$set": {"updated_at": datetime.datetime.utcnow()}
                    }
                )
                return result.modified_count > 0
            except:
                return False
        else:
            for session in _sessions_memory:
                if str(session.get('_id')) == str(session_id):
                    if 'participants' not in session:
                        session['participants'] = []
                    if user_id not in session['participants']:
                        session['participants'].append(user_id)
                        session['updated_at'] = datetime.datetime.utcnow()
                        return True
            return False

    @staticmethod
    def delete_session(session_id, user_id):
        """Delete session (only by host)"""
        if sessions_collection is not None:
            try:
                result = sessions_collection.delete_one({
                    "_id": ObjectId(session_id),
                    "host_id": user_id
                })
                return result.deleted_count > 0
            except:
                return False
        else:
            for i, session in enumerate(_sessions_memory):
                if str(session.get('_id')) == str(session_id) and session.get('host_id') == user_id:
                    del _sessions_memory[i]
                    return True
            return False
