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
        # Add SSL certificate verification bypass for development
        try:
            client = MongoClient(
                mongo_uri,
                tls=True,
                tlsAllowInvalidCertificates=True,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=10000,
                socketTimeoutMS=10000
            )
            # Test connection
            client.admin.command('ping')
            db = client.get_database("ai_chatbot_ccp")
            mood_collection = db["moods"]
            mood_suggestions_collection = db["mood_suggestions"]
            print("✅ Mood Model: Connected to MongoDB successfully with SSL")
        except Exception as ssl_error:
            print(f"⚠️ Mood Model: SSL connection failed: {ssl_error}")
            print("⚠️ Mood Model: Trying without SSL...")
            # Try without SSL
            client = MongoClient(
                mongo_uri,
                tls=False,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=10000,
                socketTimeoutMS=10000
            )
            client.admin.command('ping')
            db = client.get_database("ai_chatbot_ccp")
            mood_collection = db["moods"]
            mood_suggestions_collection = db["mood_suggestions"]
            print("✅ Mood Model: Connected to MongoDB successfully without SSL")
    else:
        # Use in-memory storage for testing
        print("⚠️ Warning: Mood Model using in-memory storage. Set MONGO_URI in .env for persistent storage.")
        mood_collection = None
        mood_suggestions_collection = None
except Exception as e:
    print(f"❌ Mood Model: MongoDB connection failed: {e}")
    print("⚠️ Mood Model: Using in-memory storage for testing.")
    mood_collection = None
    mood_suggestions_collection = None

# In-memory storage for testing
_moods_memory = []
_mood_suggestions_memory = []

class Mood:
    @staticmethod
    def get_today_mood(user_id):
        """Check if user has already submitted mood for today"""
        today = datetime.datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        tomorrow = today + datetime.timedelta(days=1)
        
        if mood_collection is not None:
            return mood_collection.find_one({
                "user_id": user_id,
                "created_at": {
                    "$gte": today,
                    "$lt": tomorrow
                }
            })
        else:
            # In-memory search
            for mood in _moods_memory:
                if (mood.get("user_id") == user_id and 
                    mood.get("created_at") and
                    mood["created_at"] >= today and 
                    mood["created_at"] < tomorrow):
                    return mood
            return None

    @staticmethod
    def create_mood_entry(user_id, mood_data):
        """Create a new mood entry"""
        created_at = datetime.datetime.utcnow()
        mood_entry = {
            'user_id': user_id,
            'mood_score': mood_data.get('mood_score'),  # 1-10 scale
            'mood_label': mood_data.get('mood_label'),  # happy, sad, anxious, etc.
            'energy_level': mood_data.get('energy_level'),  # 1-10 scale
            'stress_level': mood_data.get('stress_level'),  # 1-10 scale
            'anxiety_level': mood_data.get('anxiety_level'),  # 1-10 scale
            'sleep_quality': mood_data.get('sleep_quality'),  # 1-10 scale
            'notes': mood_data.get('notes', ''),
            'factors': mood_data.get('factors', []),  # ['work', 'relationships', 'health', etc.]
            'created_at': created_at,
            'date_str': created_at.date().isoformat()  # Store as string instead of date object
        }
        
        if mood_collection is not None:
            result = mood_collection.insert_one(mood_entry)
            mood_entry['_id'] = result.inserted_id
            return mood_entry
        else:
            # In-memory storage
            mood_id = len(_moods_memory) + 1
            mood_entry["_id"] = mood_id
            _moods_memory.append(mood_entry)
            return mood_entry

    @staticmethod
    def get_mood_history(user_id, days=30):
        """Get user's mood history for specified number of days"""
        start_date = datetime.datetime.utcnow() - datetime.timedelta(days=days)
        
        if mood_collection is not None:
            moods = list(mood_collection.find({
                "user_id": user_id,
                "created_at": {"$gte": start_date}
            }).sort("created_at", -1))
            return moods
        else:
            # In-memory search
            moods = []
            for mood in _moods_memory:
                if (mood.get("user_id") == user_id and 
                    mood.get("created_at") and
                    mood["created_at"] >= start_date):
                    moods.append(mood)
            # Sort by created_at descending
            moods.sort(key=lambda x: x.get("created_at", datetime.datetime.min), reverse=True)
            return moods

    @staticmethod
    def get_mood_analytics(user_id, days=7):
        """Get mood analytics for dashboard"""
        moods = Mood.get_mood_history(user_id, days)
        
        if not moods:
            return {
                'average_mood': 5,
                'average_energy': 5,
                'average_stress': 5,
                'mood_trend': 'stable',
                'total_entries': 0
            }
        
        total_entries = len(moods)
        avg_mood = sum(mood.get('mood_score', 5) for mood in moods) / total_entries
        avg_energy = sum(mood.get('energy_level', 5) for mood in moods) / total_entries
        avg_stress = sum(mood.get('stress_level', 5) for mood in moods) / total_entries
        
        # Determine trend
        if len(moods) >= 2:
            recent_avg = sum(mood.get('mood_score', 5) for mood in moods[:3]) / min(3, len(moods))
            older_avg = sum(mood.get('mood_score', 5) for mood in moods[-3:]) / min(3, len(moods))
            
            if recent_avg > older_avg + 0.5:
                trend = 'improving'
            elif recent_avg < older_avg - 0.5:
                trend = 'declining'
            else:
                trend = 'stable'
        else:
            trend = 'stable'
        
        return {
            'average_mood': round(avg_mood, 1),
            'average_energy': round(avg_energy, 1),
            'average_stress': round(avg_stress, 1),
            'mood_trend': trend,
            'total_entries': total_entries
        }

    @staticmethod
    def get_weekly_mood_data(user_id):
        """Get mood data for the past week for charts"""
        end_date = datetime.datetime.utcnow()
        start_date = end_date - datetime.timedelta(days=6)  # 7 days including today
        
        # Get all moods for the week
        if mood_collection is not None:
            moods = list(mood_collection.find({
                "user_id": user_id,
                "created_at": {
                    "$gte": start_date.replace(hour=0, minute=0, second=0, microsecond=0),
                    "$lte": end_date.replace(hour=23, minute=59, second=59, microsecond=999999)
                }
            }).sort("created_at", 1))
        else:
            # In-memory search
            moods = []
            for mood in _moods_memory:
                if (mood.get("user_id") == user_id and 
                    mood.get("created_at") and
                    mood["created_at"] >= start_date.replace(hour=0, minute=0, second=0, microsecond=0) and
                    mood["created_at"] <= end_date.replace(hour=23, minute=59, second=59, microsecond=999999)):
                    moods.append(mood)
            moods.sort(key=lambda x: x.get("created_at", datetime.datetime.min))
        
        # Create daily data
        daily_data = []
        for i in range(7):
            date = start_date + datetime.timedelta(days=i)
            day_name = date.strftime('%a')
            
            # Find mood for this day
            day_mood = None
            for mood in moods:
                mood_date = mood.get('created_at')
                if mood_date and mood_date.date() == date.date():
                    day_mood = mood
                    break
            
            if day_mood:
                daily_data.append({
                    'day': day_name,
                    'mood': day_mood.get('mood_score', 5),
                    'energy': day_mood.get('energy_level', 5),
                    'stress': day_mood.get('stress_level', 5),
                    'date': date.strftime('%Y-%m-%d')
                })
            else:
                daily_data.append({
                    'day': day_name,
                    'mood': None,
                    'energy': None,
                    'stress': None,
                    'date': date.strftime('%Y-%m-%d')
                })
        
        return daily_data

    @staticmethod
    def should_show_mood_prompt(user_id):
        """Check if we should show mood prompt to user"""
        today_mood = Mood.get_today_mood(user_id)
        return today_mood is None

class MoodSuggestion:
    @staticmethod
    def get_suggestions_for_mood(mood_score, stress_level, energy_level):
        """Get personalized suggestions based on mood metrics"""
        suggestions = []
        
        # Low mood suggestions
        if mood_score <= 4:
            suggestions.extend([
                {
                    'type': 'activity',
                    'title': 'Take a 10-minute walk outside',
                    'description': 'Fresh air and light exercise can help improve your mood',
                    'icon': '🚶‍♀️'
                },
                {
                    'type': 'mindfulness',
                    'title': 'Try a 5-minute breathing exercise',
                    'description': 'Deep breathing can help you feel more centered and calm',
                    'icon': '🧘‍♀️'
                },
                {
                    'type': 'social',
                    'title': 'Reach out to a friend or family member',
                    'description': 'Connection with others can help lift your spirits',
                    'icon': '💬'
                }
            ])
        
        # High stress suggestions
        if stress_level >= 7:
            suggestions.extend([
                {
                    'type': 'relaxation',
                    'title': 'Practice progressive muscle relaxation',
                    'description': 'Release physical tension to reduce stress',
                    'icon': '💆‍♀️'
                },
                {
                    'type': 'mindfulness',
                    'title': 'Listen to calming music or nature sounds',
                    'description': 'Soothing sounds can help reduce stress levels',
                    'icon': '🎵'
                },
                {
                    'type': 'activity',
                    'title': 'Write in a journal for 10 minutes',
                    'description': 'Express your thoughts to help process stress',
                    'icon': '📝'
                }
            ])
        
        # Low energy suggestions
        if energy_level <= 4:
            suggestions.extend([
                {
                    'type': 'health',
                    'title': 'Stay hydrated and have a healthy snack',
                    'description': 'Proper nutrition can help boost your energy',
                    'icon': '🥤'
                },
                {
                    'type': 'activity',
                    'title': 'Do 5 minutes of light stretching',
                    'description': 'Gentle movement can help increase energy',
                    'icon': '🤸‍♀️'
                },
                {
                    'type': 'rest',
                    'title': 'Take a 10-20 minute power nap',
                    'description': 'A short rest can help recharge your energy',
                    'icon': '😴'
                }
            ])
        
        # Good mood reinforcement
        if mood_score >= 7:
            suggestions.extend([
                {
                    'type': 'gratitude',
                    'title': 'Write down 3 things you\'re grateful for',
                    'description': 'Focusing on positives can maintain your good mood',
                    'icon': '🙏'
                },
                {
                    'type': 'social',
                    'title': 'Share your positive energy with others',
                    'description': 'Spread joy by connecting with friends or family',
                    'icon': '😊'
                }
            ])
        
        return suggestions[:4]  # Return maximum 4 suggestions

    @staticmethod
    def create_suggestion_log(user_id, suggestion_data):
        """Log when a user interacts with suggestions"""
        log_entry = {
            'user_id': user_id,
            'suggestion_type': suggestion_data.get('type'),
            'suggestion_title': suggestion_data.get('title'),
            'action': suggestion_data.get('action'),  # 'viewed', 'clicked', 'completed'
            'created_at': datetime.datetime.utcnow()
        }
        
        if mood_suggestions_collection is not None:
            result = mood_suggestions_collection.insert_one(log_entry)
            return result.inserted_id
        else:
            # In-memory storage
            log_id = len(_mood_suggestions_memory) + 1
            log_entry["_id"] = log_id
            _mood_suggestions_memory.append(log_entry)
            return log_id