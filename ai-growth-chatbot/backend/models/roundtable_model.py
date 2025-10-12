import os
import datetime
import uuid

try:
    from pymongo import MongoClient
    from bson import ObjectId
except Exception:
    MongoClient = None
    ObjectId = None

MONGO_URI = os.getenv('MONGO_URI')

# In-memory fallback storage
_sessions_memory = {}


class RoundtableSession:
    @staticmethod
    def _get_db_collection():
        """Return a pymongo collection or None if not configured."""
        if MongoClient is None or not MONGO_URI:
            return None

        try:
            client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
            db = client.get_database(os.getenv('MONGO_DB', 'ai_chatbot_ccp'))
            return db.get_collection('roundtable_sessions')
        except Exception:
            return None

    @staticmethod
    def _now():
        return datetime.datetime.utcnow()

    @staticmethod
    def get_all_sessions():
        """Return all sessions as list of dicts."""
        coll = RoundtableSession._get_db_collection()
        if coll is not None:
            docs = list(coll.find().sort('created_at', -1))
            out = []
            for d in docs:
                d['id'] = str(d.get('_id'))
                d.pop('_id', None)
                out.append(d)
            return out

        # In-memory
        return [v for k, v in sorted(_sessions_memory.items(), key=lambda x: x[1].get('created_at'), reverse=True)]

    @staticmethod
    def create_session(session_data):
        """Create a new session and return the session dict."""
        now = RoundtableSession._now()
        session = {
            'title': session_data.get('title') or 'Untitled Session',
            'description': session_data.get('description') or '',
            'date': session_data.get('date'),
            'time': session_data.get('time'),
            'maxParticipants': int(session_data.get('maxParticipants', 10)),
            'moderator': session_data.get('moderator', ''),
            'category': session_data.get('category', ''),
            'host_id': session_data.get('host_id'),
            'participants': list(session_data.get('participants', [])),
            'status': session_data.get('status', 'scheduled'),
            'created_at': now,
            'updated_at': now
        }

        coll = RoundtableSession._get_db_collection()
        if coll is not None:
            res = coll.insert_one(session)
            session['id'] = str(res.inserted_id)
            return session

        # In-memory
        sid = str(uuid.uuid4())
        session['id'] = sid
        _sessions_memory[sid] = session
        return session

    @staticmethod
    def find_by_id(session_id):
        coll = RoundtableSession._get_db_collection()
        if coll is not None:
            try:
                obj_id = ObjectId(session_id) if ObjectId is not None else session_id
                doc = coll.find_one({'_id': obj_id})
                if not doc:
                    return None
                doc['id'] = str(doc.get('_id'))
                doc.pop('_id', None)
                return doc
            except Exception:
                return None

        return _sessions_memory.get(session_id)

    @staticmethod
    def join_session(session_id, user_id):
        """Add a user to session participants. Returns True on success."""
        coll = RoundtableSession._get_db_collection()
        now = RoundtableSession._now()
        if coll is not None:
            try:
                obj_id = ObjectId(session_id) if ObjectId is not None else session_id
                doc = coll.find_one({'_id': obj_id})
                if not doc:
                    return False
                participants = doc.get('participants', [])
                if user_id in participants:
                    return False
                participants.append(user_id)
                coll.update_one({'_id': obj_id}, {'$set': {'participants': participants, 'updated_at': now}})
                return True
            except Exception:
                return False

        # In-memory
        s = _sessions_memory.get(session_id)
        if not s:
            return False
        if user_id in s.get('participants', []):
            return False
        s['participants'].append(user_id)
        s['updated_at'] = now
        return True

    @staticmethod
    def update_status(session_id, status):
        coll = RoundtableSession._get_db_collection()
        now = RoundtableSession._now()
        if coll is not None:
            try:
                obj_id = ObjectId(session_id) if ObjectId is not None else session_id
                res = coll.update_one({'_id': obj_id}, {'$set': {'status': status, 'updated_at': now}})
                return res.matched_count > 0
            except Exception:
                return False

        s = _sessions_memory.get(session_id)
        if not s:
            return False
        s['status'] = status
        s['updated_at'] = now
        return True

    @staticmethod
    def delete_session(session_id, user_id):
        """Delete a session only if user_id is the host. Returns True on success."""
        coll = RoundtableSession._get_db_collection()
        if coll is not None:
            try:
                obj_id = ObjectId(session_id) if ObjectId is not None else session_id
                doc = coll.find_one({'_id': obj_id})
                if not doc:
                    return False
                if doc.get('host_id') != user_id:
                    return False
                coll.delete_one({'_id': obj_id})
                return True
            except Exception:
                return False

        s = _sessions_memory.get(session_id)
        if not s:
            return False
        if s.get('host_id') != user_id:
            return False
        del _sessions_memory[session_id]
        return True
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
