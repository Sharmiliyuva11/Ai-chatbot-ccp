from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify
from models.user_model import User
from functools import wraps

def token_required(f):
    """
    Decorator to require JWT token for protected routes.
    Extracts user from JWT token and passes it to the route function.
    """
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        try:
            user_id = get_jwt_identity()
            current_user = User.find_by_id(user_id)

            if not current_user:
                return jsonify({
                    'success': False,
                    'message': 'User not found'
                }), 404

            # Pass the current_user to the route function
            return f(current_user=current_user, *args, **kwargs)
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'Token validation failed',
                'error': str(e)
            }), 401

    return decorated_function
