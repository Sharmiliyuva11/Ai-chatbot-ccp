from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.roundtable_model import RoundtableSession

roundtable_bp = Blueprint('roundtable', __name__)

@roundtable_bp.route('/sessions', methods=['GET'])
@jwt_required()
def get_sessions():
    user_id = get_jwt_identity()
    # Get all sessions for all users (so users can see and join others' sessions)
    sessions = RoundtableSession.get_all_sessions()

    # Mark which sessions are hosted by the current user and which they've joined
    for session in sessions:
        session['is_host'] = (session.get('host_id') == user_id)
        session['joined'] = user_id in session.get('participants', [])

    return jsonify({'success': True, 'sessions': sessions})

@roundtable_bp.route('/sessions', methods=['POST'])
@jwt_required()
def create_session():
    user_id = get_jwt_identity()
    data = request.get_json()

    session_data = {
        'title': data.get('title'),
        'description': data.get('description'),
        'date': data.get('date'),
        'time': data.get('time'),
        'maxParticipants': data.get('maxParticipants', 10),
        'moderator': data.get('moderator', 'You'),
        'category': data.get('category', ''),
        'host_id': user_id,
        'participants': [user_id],
        'status': 'scheduled'
    }

    session = RoundtableSession.create_session(session_data)
    return jsonify({'success': True, 'session': session})

@roundtable_bp.route('/sessions/<session_id>/join', methods=['POST'])
@jwt_required()
def join_session(session_id):
    user_id = get_jwt_identity()

    # Check if session exists and user can join
    session = RoundtableSession.find_by_id(session_id)
    if not session:
        return jsonify({'success': False, 'message': 'Session not found'}), 404

    # Check if session is full
    if len(session.get('participants', [])) >= session.get('maxParticipants', 10):
        return jsonify({'success': False, 'message': 'Session is full'}), 400

    # Check if user is already a participant
    if user_id in session.get('participants', []):
        return jsonify({'success': False, 'message': 'Already joined this session'}), 400

    # Add user to participants
    success = RoundtableSession.join_session(session_id, user_id)
    if success:
        # Get updated session
        updated_session = RoundtableSession.find_by_id(session_id)
        return jsonify({'success': True, 'session': updated_session})
    else:
        return jsonify({'success': False, 'message': 'Failed to join session'}), 500

@roundtable_bp.route('/sessions/<session_id>', methods=['DELETE'])
@jwt_required()
def delete_session(session_id):
    user_id = get_jwt_identity()

    success = RoundtableSession.delete_session(session_id, user_id)
    if success:
        return jsonify({'success': True, 'message': 'Session deleted successfully'})
    else:
        return jsonify({'success': False, 'message': 'Session not found or not authorized'}), 404
