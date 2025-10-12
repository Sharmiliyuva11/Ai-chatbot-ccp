from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.mindspace_model import MindSpaceModel
import os
import requests
import time

# Blueprint for mindspace routes
mindspace_bp = Blueprint('mindspace', __name__)
mindspace_model = MindSpaceModel()

@mindspace_bp.route('/sessions', methods=['GET'])
def get_sessions():
    """Get all mindspace sessions"""
    try:
        category = request.args.get('category', 'all')
        sessions = mindspace_model.get_all_sessions(category)
        
        return jsonify({
            "success": True,
            "sessions": sessions
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error fetching sessions: {str(e)}"
        }), 500

@mindspace_bp.route('/sessions/<int:session_id>', methods=['GET'])
def get_session(session_id):
    """Get a specific session by ID"""
    try:
        session = mindspace_model.get_session_by_id(session_id)
        
        if not session:
            return jsonify({
                "success": False,
                "message": "Session not found"
            }), 404
            
        return jsonify({
            "success": True,
            "session": session
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error fetching session: {str(e)}"
        }), 500

@mindspace_bp.route('/categories', methods=['GET'])
def get_categories():
    """Get all mindspace categories"""
    try:
        categories = mindspace_model.get_categories()
        # Add 'all' category at the beginning
        categories.insert(0, {"id": "all", "name": "All", "description": "All categories", "icon": "brain", "color": "#6366f1"})
        
        return jsonify({
            "success": True,
            "categories": categories
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error fetching categories: {str(e)}"
        }), 500

@mindspace_bp.route('/sessions/<int:session_id>/start', methods=['POST'])
@jwt_required()
def start_session(session_id):
    """Start a session for the current user"""
    try:
        user_id = get_jwt_identity()
        session_record_id = mindspace_model.start_session(user_id, session_id)
        
        return jsonify({
            "success": True,
            "session_record_id": session_record_id,
            "message": "Session started successfully"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error starting session: {str(e)}"
        }), 500

@mindspace_bp.route('/sessions/<int:session_id>/progress', methods=['POST'])
@jwt_required()
def update_progress(session_id):
    """Update session progress"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        progress_seconds = data.get('progress_seconds', 0)
        
        mindspace_model.update_session_progress(user_id, session_id, progress_seconds)
        
        return jsonify({
            "success": True,
            "message": "Progress updated successfully"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error updating progress: {str(e)}"
        }), 500

@mindspace_bp.route('/sessions/<int:session_id>/complete', methods=['POST'])
@jwt_required()
def complete_session(session_id):
    """Mark a session as completed"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        rating = data.get('rating')
        notes = data.get('notes')
        
        success = mindspace_model.complete_session(user_id, session_id, rating, notes)
        
        if success:
            return jsonify({
                "success": True,
                "message": "Session completed successfully"
            })
        else:
            return jsonify({
                "success": False,
                "message": "Session not found or already completed"
            }), 404
            
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error completing session: {str(e)}"
        }), 500

@mindspace_bp.route('/progress', methods=['GET'])
@jwt_required()
def get_user_progress():
    """Get current user's progress"""
    try:
        user_id = get_jwt_identity()
        progress = mindspace_model.get_user_progress(user_id)
        
        return jsonify({
            "success": True,
            "progress": progress
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error fetching progress: {str(e)}"
        }), 500

@mindspace_bp.route('/history', methods=['GET'])
@jwt_required()
def get_session_history():
    """Get current user's session history"""
    try:
        user_id = get_jwt_identity()
        limit = request.args.get('limit', 10, type=int)
        history = mindspace_model.get_user_session_history(user_id, limit)
        
        return jsonify({
            "success": True,
            "history": history
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error fetching history: {str(e)}"
        }), 500

@mindspace_bp.route('/scrape-external', methods=['POST'])
@jwt_required()
def scrape_external_content():
    """Scrape external meditation resources (placeholder for future implementation)"""
    try:
        # This is a placeholder for external content scraping
        # In the future, you can implement scraping from meditation APIs like:
        # - Insight Timer API
        # - Headspace API (if available)
        # - Calm API
        # - YouTube meditation content
        
        # For now, return a mock response
        external_content = [
            {
                "id": "ext_1",
                "title": "External Guided Meditation",
                "description": "Sample external content from meditation API",
                "duration": "15 min",
                "category": "meditation",
                "source": "external_api",
                "url": "https://example.com/meditation",
                "rating": 4.5
            }
        ]
        
        return jsonify({
            "success": True,
            "external_content": external_content,
            "message": "External content fetched successfully"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error scraping external content: {str(e)}"
        }), 500

@mindspace_bp.route('/personalized-recommendations', methods=['GET'])
@jwt_required()
def get_personalized_recommendations():
    """Get AI-based personalized recommendations (basic implementation)"""
    try:
        user_id = get_jwt_identity()
        progress = mindspace_model.get_user_progress(user_id)
        history = mindspace_model.get_user_session_history(user_id, 5)
        
        # Simple recommendation logic based on user's favorite category and progress
        favorite_category = progress.get('favorite_category', 'meditation')
        
        # Get sessions from favorite category
        recommended_sessions = mindspace_model.get_all_sessions(favorite_category.lower())
        
        # Filter out recently completed sessions
        recent_session_ids = [h['session_id'] for h in history]
        recommended_sessions = [s for s in recommended_sessions if s['id'] not in recent_session_ids]
        
        # Limit to top 3 recommendations
        recommended_sessions = recommended_sessions[:3]
        
        return jsonify({
            "success": True,
            "recommendations": recommended_sessions,
            "reason": f"Based on your favorite category: {favorite_category}"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error fetching recommendations: {str(e)}"
        }), 500