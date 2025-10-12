from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.mood_model import Mood, MoodSuggestion
import datetime

mood_bp = Blueprint('mood', __name__)

@mood_bp.route('/check-prompt', methods=['GET'])
@jwt_required()
def check_mood_prompt():
    """Check if user should see mood prompt for today"""
    try:
        user_id = get_jwt_identity()
        should_prompt = Mood.should_show_mood_prompt(user_id)
        
        return jsonify({
            'success': True,
            'show_prompt': should_prompt
        })
        
    except Exception as e:
        print(f"Error checking mood prompt: {e}")
        return jsonify({
            'success': False,
            'message': 'Failed to check mood prompt',
            'show_prompt': False
        }), 500

@mood_bp.route('/submit', methods=['POST'])
@jwt_required()
def submit_mood():
    """Submit daily mood data"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['mood_score', 'mood_label']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'message': f'Missing required field: {field}'
                }), 400
        
        # Check if user already submitted mood today
        today_mood = Mood.get_today_mood(user_id)
        if today_mood:
            return jsonify({
                'success': False,
                'message': 'You have already submitted your mood for today'
            }), 400
        
        # Validate mood score range
        mood_score = data.get('mood_score')
        if not isinstance(mood_score, (int, float)) or mood_score < 1 or mood_score > 10:
            return jsonify({
                'success': False,
                'message': 'Mood score must be between 1 and 10'
            }), 400
        
        # Create mood entry
        mood_data = {
            'mood_score': mood_score,
            'mood_label': data.get('mood_label'),
            'energy_level': data.get('energy_level', 5),
            'stress_level': data.get('stress_level', 5),
            'anxiety_level': data.get('anxiety_level', 5),
            'sleep_quality': data.get('sleep_quality', 5),
            'notes': data.get('notes', ''),
            'factors': data.get('factors', [])
        }
        
        mood_entry = Mood.create_mood_entry(user_id, mood_data)
        
        # Get personalized suggestions based on mood
        suggestions = MoodSuggestion.get_suggestions_for_mood(
            mood_score, 
            mood_data.get('stress_level', 5),
            mood_data.get('energy_level', 5)
        )
        
        return jsonify({
            'success': True,
            'message': 'Mood submitted successfully',
            'mood_entry': {
                'id': str(mood_entry['_id']),
                'mood_score': mood_entry['mood_score'],
                'mood_label': mood_entry['mood_label'],
                'created_at': mood_entry['created_at'].isoformat()
            },
            'suggestions': suggestions
        })
        
    except Exception as e:
        print(f"Error submitting mood: {e}")
        return jsonify({
            'success': False,
            'message': 'Failed to submit mood data'
        }), 500

@mood_bp.route('/today', methods=['GET'])
@jwt_required()
def get_today_mood():
    """Get today's mood entry"""
    try:
        user_id = get_jwt_identity()
        mood = Mood.get_today_mood(user_id)
        
        if mood:
            return jsonify({
                'success': True,
                'mood': {
                    'id': str(mood['_id']),
                    'mood_score': mood['mood_score'],
                    'mood_label': mood['mood_label'],
                    'energy_level': mood.get('energy_level'),
                    'stress_level': mood.get('stress_level'),
                    'anxiety_level': mood.get('anxiety_level'),
                    'sleep_quality': mood.get('sleep_quality'),
                    'notes': mood.get('notes', ''),
                    'factors': mood.get('factors', []),
                    'created_at': mood['created_at'].isoformat()
                }
            })
        else:
            return jsonify({
                'success': True,
                'mood': None,
                'message': 'No mood entry for today'
            })
            
    except Exception as e:
        print(f"Error getting today's mood: {e}")
        return jsonify({
            'success': False,
            'message': 'Failed to get today\'s mood'
        }), 500

@mood_bp.route('/history', methods=['GET'])
@jwt_required()
def get_mood_history():
    """Get mood history for specified number of days"""
    try:
        user_id = get_jwt_identity()
        days = request.args.get('days', default=30, type=int)
        
        # Validate days parameter
        if days < 1 or days > 365:
            return jsonify({
                'success': False,
                'message': 'Days parameter must be between 1 and 365'
            }), 400
        
        moods = Mood.get_mood_history(user_id, days)
        
        # Format mood data for response
        mood_data = []
        for mood in moods:
            mood_data.append({
                'id': str(mood['_id']),
                'mood_score': mood['mood_score'],
                'mood_label': mood['mood_label'],
                'energy_level': mood.get('energy_level'),
                'stress_level': mood.get('stress_level'),
                'anxiety_level': mood.get('anxiety_level'),
                'sleep_quality': mood.get('sleep_quality'),
                'notes': mood.get('notes', ''),
                'factors': mood.get('factors', []),
                'created_at': mood['created_at'].isoformat(),
                'date': mood['created_at'].date().isoformat()
            })
        
        return jsonify({
            'success': True,
            'moods': mood_data,
            'total_count': len(mood_data)
        })
        
    except Exception as e:
        print(f"Error getting mood history: {e}")
        return jsonify({
            'success': False,
            'message': 'Failed to get mood history'
        }), 500

@mood_bp.route('/analytics', methods=['GET'])
@jwt_required()
def get_mood_analytics():
    """Get mood analytics for dashboard"""
    try:
        user_id = get_jwt_identity()
        days = request.args.get('days', default=7, type=int)
        
        # Get analytics data
        analytics = Mood.get_mood_analytics(user_id, days)
        
        return jsonify({
            'success': True,
            'analytics': analytics
        })
        
    except Exception as e:
        print(f"Error getting mood analytics: {e}")
        return jsonify({
            'success': False,
            'message': 'Failed to get mood analytics'
        }), 500

@mood_bp.route('/weekly-chart', methods=['GET'])
@jwt_required()
def get_weekly_mood_chart():
    """Get mood data for weekly chart"""
    try:
        user_id = get_jwt_identity()
        chart_data = Mood.get_weekly_mood_data(user_id)
        
        return jsonify({
            'success': True,
            'chart_data': chart_data
        })
        
    except Exception as e:
        print(f"Error getting weekly mood chart: {e}")
        return jsonify({
            'success': False,
            'message': 'Failed to get weekly mood chart data'
        }), 500

@mood_bp.route('/suggestions', methods=['POST'])
@jwt_required()
def get_mood_suggestions():
    """Get personalized mood suggestions"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Get current mood data or use provided data
        mood_score = data.get('mood_score', 5)
        stress_level = data.get('stress_level', 5)
        energy_level = data.get('energy_level', 5)
        
        # If no data provided, try to get today's mood
        if not data or all(key not in data for key in ['mood_score', 'stress_level', 'energy_level']):
            today_mood = Mood.get_today_mood(user_id)
            if today_mood:
                mood_score = today_mood.get('mood_score', 5)
                stress_level = today_mood.get('stress_level', 5)
                energy_level = today_mood.get('energy_level', 5)
        
        suggestions = MoodSuggestion.get_suggestions_for_mood(
            mood_score, stress_level, energy_level
        )
        
        return jsonify({
            'success': True,
            'suggestions': suggestions,
            'based_on': {
                'mood_score': mood_score,
                'stress_level': stress_level,
                'energy_level': energy_level
            }
        })
        
    except Exception as e:
        print(f"Error getting mood suggestions: {e}")
        return jsonify({
            'success': False,
            'message': 'Failed to get mood suggestions'
        }), 500

@mood_bp.route('/suggestion-action', methods=['POST'])
@jwt_required()
def log_suggestion_action():
    """Log user interaction with mood suggestions"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate required fields
        if not data or 'action' not in data:
            return jsonify({
                'success': False,
                'message': 'Missing required field: action'
            }), 400
        
        suggestion_data = {
            'type': data.get('type'),
            'title': data.get('title'),
            'action': data.get('action')  # 'viewed', 'clicked', 'completed'
        }
        
        log_id = MoodSuggestion.create_suggestion_log(user_id, suggestion_data)
        
        return jsonify({
            'success': True,
            'message': 'Action logged successfully',
            'log_id': str(log_id)
        })
        
    except Exception as e:
        print(f"Error logging suggestion action: {e}")
        return jsonify({
            'success': False,
            'message': 'Failed to log suggestion action'
        }), 500

@mood_bp.route('/dashboard-status', methods=['GET'])
@jwt_required()
def get_dashboard_mood_status():
    """Get mood status and suggestions for dashboard display"""
    try:
        user_id = get_jwt_identity()
        
        # Check if user should be prompted for mood
        should_prompt = Mood.should_show_mood_prompt(user_id)
        
        if should_prompt:
            return jsonify({
                'success': True,
                'status': 'prompt_needed',
                'message': 'How are you feeling today?',
                'show_prompt': True,
                'suggestions': []
            })
        
        # Get today's mood and generate suggestions
        today_mood = Mood.get_today_mood(user_id)
        if today_mood:
            suggestions = MoodSuggestion.get_suggestions_for_mood(
                today_mood.get('mood_score', 5),
                today_mood.get('stress_level', 5),
                today_mood.get('energy_level', 5)
            )
            
            # Determine if we should show suggestions popup
            show_suggestions = today_mood.get('mood_score', 5) <= 4 or today_mood.get('stress_level', 5) >= 7
            
            return jsonify({
                'success': True,
                'status': 'mood_recorded',
                'mood': {
                    'score': today_mood.get('mood_score'),
                    'label': today_mood.get('mood_label'),
                    'stress_level': today_mood.get('stress_level'),
                    'energy_level': today_mood.get('energy_level')
                },
                'show_prompt': False,
                'show_suggestions': show_suggestions,
                'suggestions': suggestions[:3] if show_suggestions else []  # Limit to 3 for popup
            })
        
        return jsonify({
            'success': True,
            'status': 'no_data',
            'show_prompt': False,
            'suggestions': []
        })
        
    except Exception as e:
        print(f"Error getting dashboard mood status: {e}")
        return jsonify({
            'success': False,
            'message': 'Failed to get dashboard mood status'
        }), 500