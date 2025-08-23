from flask import Blueprint, jsonify

# Blueprint for mindspace routes
mindspace_bp = Blueprint('mindspace', __name__)

@mindspace_bp.route('/sessions', methods=['GET'])
def get_sessions():
    """Get all mindspace sessions"""
    sessions = [
        {
            "id": 1,
            "title": "Morning Mindfulness",
            "description": "Start your day with clarity and intention through guided mindfulness practice.",
            "duration": "10 min",
            "category": "meditation",
            "difficulty": "Beginner",
            "instructor": "Sarah Chen",
            "image": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=300&h=200&fit=crop",
            "audio": "/audio/morning-mindfulness.mp3",
            "plays": 1250,
            "rating": 4.8
        },
        {
            "id": 2,
            "title": "Deep Focus Flow",
            "description": "Enhance concentration and productivity with binaural beats and ambient sounds.",
            "duration": "25 min",
            "category": "focus",
            "difficulty": "Intermediate",
            "instructor": "Michael Torres",
            "image": "https://images.unsplash.com/photo-1499209974431-9dddcece7f88?w=300&h=200&fit=crop",
            "audio": "/audio/deep-focus.mp3",
            "plays": 890,
            "rating": 4.9
        },
        {
            "id": 3,
            "title": "Peaceful Sleep Journey",
            "description": "Drift into restful sleep with calming narration and gentle soundscapes.",
            "duration": "30 min",
            "category": "sleep",
            "difficulty": "Beginner",
            "instructor": "Emma Wilson",
            "image": "https://images.unsplash.com/photo-1517147177326-b37599372b73?w=300&h=200&fit=crop",
            "audio": "/audio/sleep-journey.mp3",
            "plays": 2100,
            "rating": 4.7
        },
        {
            "id": 4,
            "title": "Energy Boost Meditation",
            "description": "Revitalize your mind and body with energizing breathing techniques.",
            "duration": "15 min",
            "category": "energy",
            "difficulty": "Intermediate",
            "instructor": "David Kim",
            "image": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=300&h=200&fit=crop",
            "audio": "/audio/energy-boost.mp3",
            "plays": 675,
            "rating": 4.6
        },
        {
            "id": 5,
            "title": "Forest Sounds Relaxation",
            "description": "Immerse yourself in the tranquil sounds of nature for deep relaxation.",
            "duration": "45 min",
            "category": "nature",
            "difficulty": "Beginner",
            "instructor": "Nature Sounds",
            "image": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=300&h=200&fit=crop",
            "audio": "/audio/forest-sounds.mp3",
            "plays": 1800,
            "rating": 4.9
        },
        {
            "id": 6,
            "title": "Ocean Waves Meditation",
            "description": "Let the rhythmic sounds of ocean waves guide you to inner peace.",
            "duration": "20 min",
            "category": "nature",
            "difficulty": "Beginner",
            "instructor": "Ocean Sounds",
            "image": "https://images.unsplash.com/photo-1505142468610-359e7d316be0?w=300&h=200&fit=crop",
            "audio": "/audio/ocean-waves.mp3",
            "plays": 1450,
            "rating": 4.8
        }
    ]
    
    return jsonify({
        "success": True,
        "sessions": sessions
    })

@mindspace_bp.route('/categories', methods=['GET'])
def get_categories():
    """Get all mindspace categories"""
    categories = [
        {"id": "all", "name": "All"},
        {"id": "meditation", "name": "Meditation"},
        {"id": "focus", "name": "Focus"},
        {"id": "sleep", "name": "Sleep"},
        {"id": "energy", "name": "Energy"},
        {"id": "nature", "name": "Nature"}
    ]
    
    return jsonify({
        "success": True,
        "categories": categories
    })