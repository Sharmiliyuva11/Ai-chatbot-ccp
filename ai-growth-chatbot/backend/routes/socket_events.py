from app import socketio
from flask_jwt_extended import decode_token
from flask import request


@socketio.on('connect')
def on_connect():
    # Optionally verify token from query string
    token = request.args.get('token')
    if token:
        try:
            decoded = decode_token(token)
            user_id = decoded.get('sub') or decoded.get('identity') or decoded.get('user_id')
            if user_id:
                socketio.enter_room(request.sid, f'user-{user_id}')
        except Exception:
            # Invalid token — do not join room
            pass


@socketio.on('join_user_room')
def handle_join_user_room(data):
    # data: { userId }
    user_id = data.get('userId')
    if user_id:
        try:
            socketio.enter_room(request.sid, f'user-{user_id}')
        except Exception:
            pass
