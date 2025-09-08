from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

roundtable_bp = Blueprint('roundtable', __name__)

# In-memory session store for demo
_sessions = []

@roundtable_bp.route('/sessions', methods=['GET'])
@jwt_required()
def get_sessions():
    user_id = get_jwt_identity()
    # Return all sessions, marking which are hosted by the user
    for s in _sessions:
        s['is_host'] = (s['host_id'] == user_id)
        s['joined'] = user_id in s.get('participants', [])
    return jsonify({'success': True, 'sessions': _sessions})

@roundtable_bp.route('/sessions', methods=['POST'])
@jwt_required()
def create_session():
    user_id = get_jwt_identity()
    data = request.get_json()
    session = {
        'id': str(len(_sessions) + 1),
        'title': data.get('title'),
        'description': data.get('description'),
        'date': data.get('date'),
        'time': data.get('time'),
        'maxParticipants': data.get('maxParticipants', 10),
        'moderator': data.get('moderator', 'You'),
        'category': data.get('category', ''),
        'host_id': user_id,
        'participants': [user_id],
        'status': 'scheduled',
        'created_at': datetime.utcnow().isoformat()
    }
    _sessions.append(session)
    return jsonify({'success': True, 'session': session})

@roundtable_bp.route('/sessions/<session_id>/join', methods=['POST'])
@jwt_required()
def join_session(session_id):
    user_id = get_jwt_identity()
    for s in _sessions:
        if s['id'] == session_id:
            if user_id not in s['participants']:
                s['participants'].append(user_id)
                # TODO: Notify conductor/host (e.g., send email)
            return jsonify({'success': True, 'session': s})
    return jsonify({'success': False, 'message': 'Session not found'}), 404
