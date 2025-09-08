from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from pymongo import MongoClient
from datetime import datetime, timedelta
from models.user_model import User
import os
from dotenv import load_dotenv
from bson import ObjectId

load_dotenv()

# MongoDB setup
try:
    mongo_uri = os.getenv("MONGO_URI")
    if mongo_uri and mongo_uri != "mongodb+srv://<username>:<password>@cluster0.mongodb.net/?retryWrites=true&w=majority":
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        db = client.get_database("ai_chatbot_ccp")
        chats_collection = db["chats"]
        reminders_collection = db["reminders"]
        print("✅ Analytics: Connected to MongoDB successfully")
    else:
        print("⚠️ Analytics: Using in-memory storage. Set MONGO_URI in .env for persistent storage.")
        chats_collection = None
        reminders_collection = None
except Exception as e:
    print(f"❌ Analytics: MongoDB connection failed: {e}")
    chats_collection = None
    reminders_collection = None

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/dashboard-stats', methods=['GET'])
@jwt_required()
def get_dashboard_stats():
    """Get dashboard statistics for the authenticated user"""
    user_id = get_jwt_identity()
    
    try:
        # Get user info
        user = User.find_by_id(user_id)
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        # Calculate stats
        stats = {
            'chatSessions': 0,
            'activeTasks': 0,
            'meditationSessions': 0,
            'communityGroups': 0,
            'mood': 8,
            'stress': 1,
            'daysActive': 0
        }
        
        # Get chat sessions count
        if chats_collection is not None:
            stats['chatSessions'] = chats_collection.count_documents({"user_id": user_id})
        
        # Get active reminders count
        if reminders_collection is not None:
            current_time = datetime.utcnow()
            stats['activeTasks'] = reminders_collection.count_documents({
                "user_id": user_id,
                "remind_at": {"$gte": current_time}
            })
        
        # Calculate days active (days since user creation)
        if user.get('created_at'):
            created_at = user['created_at']
            if isinstance(created_at, str):
                # Handle string dates
                try:
                    created_at = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                except:
                    created_at = datetime.utcnow()
            stats['daysActive'] = (datetime.utcnow() - created_at).days
        
        # For now, set meditation and community to 0 (can be extended later)
        stats['meditationSessions'] = 0
        stats['communityGroups'] = 0
        
        return jsonify({
            'success': True,
            'stats': stats
        })
        
    except Exception as e:
        print(f"Error getting dashboard stats: {e}")
        return jsonify({'success': False, 'message': 'Failed to fetch dashboard statistics'}), 500

@analytics_bp.route('/recent-activity', methods=['GET'])
@jwt_required()
def get_recent_activity():
    """Get recent user activity"""
    user_id = get_jwt_identity()
    
    try:
        activities = []
        
        # Get recent chats
        if chats_collection is not None:
            recent_chats = list(chats_collection.find(
                {"user_id": user_id}
            ).sort("timestamp", -1).limit(3))
            
            for chat in recent_chats:
                activities.append({
                    'type': 'chat',
                    'title': 'AI Chat Session',
                    'time': chat['timestamp'].strftime('%Y-%m-%d %H:%M:%S') if chat.get('timestamp') else 'Unknown',
                    'status': 'completed',
                    'color': 'blue'
                })
        
        # Get recent reminders
        if reminders_collection is not None:
            recent_reminders = list(reminders_collection.find(
                {"user_id": user_id}
            ).sort("created_at", -1).limit(2))
            
            for reminder in recent_reminders:
                activities.append({
                    'type': 'reminder',
                    'title': reminder.get('title', 'Task Reminder'),
                    'time': reminder['created_at'].strftime('%Y-%m-%d %H:%M:%S') if reminder.get('created_at') else 'Unknown',
                    'status': 'pending' if reminder.get('remind_at', datetime.utcnow()) > datetime.utcnow() else 'completed',
                    'color': 'green'
                })
        
        # Sort activities by time (most recent first)
        activities.sort(key=lambda x: x['time'], reverse=True)
        
        # Limit to 5 most recent activities
        activities = activities[:5]
        
        return jsonify({
            'success': True,
            'activities': activities
        })
        
    except Exception as e:
        print(f"Error getting recent activity: {e}")
        return jsonify({'success': False, 'message': 'Failed to fetch recent activity'}), 500

@analytics_bp.route('/mood-data', methods=['GET'])
@jwt_required()
def get_mood_data():
    """Get mood data for charts (placeholder data for now)"""
    user_id = get_jwt_identity()
    
    try:
        # For now, return sample data
        # This can be extended with actual mood tracking functionality
        mood_data = [
            {'day': 'Mon', 'value': 7},
            {'day': 'Tue', 'value': 8},
            {'day': 'Wed', 'value': 6},
            {'day': 'Thu', 'value': 9},
            {'day': 'Fri', 'value': 7},
            {'day': 'Sat', 'value': 8},
            {'day': 'Sun', 'value': 9}
        ]
        
        activity_data = [65, 78, 45, 89, 67, 78, 92]
        
        return jsonify({
            'success': True,
            'moodData': mood_data,
            'activityData': activity_data
        })
        
    except Exception as e:
        print(f"Error getting mood data: {e}")
        return jsonify({'success': False, 'message': 'Failed to fetch mood data'}), 500

@analytics_bp.route('/user-profile', methods=['GET'])
@jwt_required()
def get_user_profile_stats():
    """Get user profile statistics"""
    user_id = get_jwt_identity()
    
    try:
        user = User.find_by_id(user_id)
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        # Calculate profile stats
        stats = {
            'daysActive': 0,
            'goalsCompleted': 0,
            'moodStreak': 7,
            'sessions': 0
        }
        
        # Calculate days active
        if user.get('created_at'):
            created_at = user['created_at']
            if isinstance(created_at, str):
                try:
                    created_at = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                except:
                    created_at = datetime.utcnow()
            stats['daysActive'] = (datetime.utcnow() - created_at).days
        
        # Get chat sessions count
        if chats_collection is not None:
            stats['sessions'] = chats_collection.count_documents({"user_id": user_id})
        
        # Get completed reminders as goals
        if reminders_collection is not None:
            current_time = datetime.utcnow()
            stats['goalsCompleted'] = reminders_collection.count_documents({
                "user_id": user_id,
                "remind_at": {"$lt": current_time}
            })
        
        return jsonify({
            'success': True,
            'stats': stats
        })
        
    except Exception as e:
        print(f"Error getting user profile stats: {e}")
        return jsonify({'success': False, 'message': 'Failed to fetch profile statistics'}), 500