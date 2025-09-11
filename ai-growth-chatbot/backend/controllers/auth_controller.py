from flask import Blueprint, request, jsonify, redirect, session
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from models.user_model import User
from services.email_service import email_service
import os
import re
from authlib.integrations.flask_client import OAuth
from urllib.parse import urlencode
import requests
import secrets

auth_bp = Blueprint('auth', __name__)

# Initialize OAuth (Google)
oauth = OAuth()

def init_oauth(app):
    """Initialize OAuth with app instance"""
    oauth.init_app(app)
    
    google = oauth.register(
        name='google',
        client_id=os.getenv('GOOGLE_CLIENT_ID'),
        client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
        client_kwargs={
            'scope': 'openid email profile'
        },
        server_metadata_url='https://accounts.google.com/.well-known/openid_configuration'
    )
    return google

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    if len(password) < 3:
        return False, "Password must be at least 3 characters long"
    return True, ""

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not all([name, email, password]):
        return jsonify({'success': False, 'message': 'All fields are required'}), 400

    # Validate email format
    if not validate_email(email):
        return jsonify({'success': False, 'message': 'Invalid email format'}), 400

    # Validate password
    is_valid, message = validate_password(password)
    if not is_valid:
        return jsonify({'success': False, 'message': message}), 400

    # Check if user already exists
    if User.find_by_email(email):
        return jsonify({'success': False, 'message': 'User already exists with this email'}), 400

    # Generate username from email
    username = email.split('@')[0]
    base_username = username
    counter = 1
    
    # Ensure username is unique
    while User.find_by_username(username):
        username = f"{base_username}{counter}"
        counter += 1

    hashed_password = generate_password_hash(password)
    new_user = {
        'name': name,
        'email': email,
        'username': username,
        'password': hashed_password
    }

    user_id = User.create_user(new_user)
    
    if user_id is None:
        return jsonify({'success': False, 'message': 'Registration failed'}), 400

    # Send welcome email (don't fail registration if email fails)
    try:
        email_service.send_welcome_email(email, name)
    except Exception as e:
        print(f"Failed to send welcome email: {e}")

    return jsonify({
    'success': True,
    'message': 'Registration successful! Welcome to Coby AI!',
        'user': {
            'id': str(user_id),
            'name': name,
            'email': email,
            'username': username
        }
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    identifier = data.get('email')  # Can be email or username
    password = data.get('password')

    if not all([identifier, password]):
        return jsonify({'success': False, 'message': 'Email/Username and password are required'}), 400

    # Find user by email or username
    user = User.verify_user(identifier, password)

    if not user:
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

    access_token = create_access_token(identity=str(user['_id']))
    return jsonify({
        'success': True,
        'message': 'Login successful',
        'token': access_token,
        'user': {
            'id': str(user['_id']),
            'name': user['name'],
            'email': user['email'],
            'username': user['username'],
            'oauth_provider': user.get('oauth_provider')
        }
    })


@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({'success': False, 'message': 'Email is required'}), 400

    if not validate_email(email):
        return jsonify({'success': False, 'message': 'Invalid email format'}), 400

    # Create password reset token
    token = User.create_password_reset_token(email)
    
    if token:
        user = User.find_by_email(email)
        # Send reset email
        email_sent = email_service.send_password_reset_email(
            email, 
            token, 
            user['name'] if user else 'User'
        )
        
        if email_sent:
            return jsonify({
                'success': True,
                'message': 'Password reset link has been sent to your email'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to send reset email. Please try again.'
            }), 500
    else:
        # Don't reveal if email exists or not (security)
        return jsonify({
            'success': True,
            'message': 'If an account with this email exists, a password reset link has been sent.'
        })


@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()
    token = data.get('token')
    new_password = data.get('password')

    if not all([token, new_password]):
        return jsonify({'success': False, 'message': 'Token and new password are required'}), 400

    # Validate password
    is_valid, message = validate_password(new_password)
    if not is_valid:
        return jsonify({'success': False, 'message': message}), 400

    # Use reset token
    if User.use_reset_token(token, new_password):
        return jsonify({
            'success': True,
            'message': 'Password has been reset successfully'
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Invalid or expired reset token'
        }), 400


@auth_bp.route('/verify-reset-token', methods=['POST'])
def verify_reset_token():
    data = request.get_json()
    token = data.get('token')

    if not token:
        return jsonify({'success': False, 'message': 'Token is required'}), 400

    token_doc = User.verify_reset_token(token)
    
    if token_doc:
        return jsonify({
            'success': True,
            'message': 'Token is valid'
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Invalid or expired token'
        }), 400


# Google OAuth Routes
@auth_bp.route('/google', methods=['GET'])
def google_login():
    """Redirect to Google OAuth"""
    redirect_uri = os.getenv('GOOGLE_REDIRECT_URI')
    
    # Build Google OAuth URL manually for better control
    base_url = 'https://accounts.google.com/o/oauth2/auth'
    params = {
        'client_id': os.getenv('GOOGLE_CLIENT_ID'),
        'redirect_uri': redirect_uri,
        'scope': 'openid email profile',
        'response_type': 'code',
        'access_type': 'offline',
        'prompt': 'select_account'
    }
    
    google_auth_url = f"{base_url}?{urlencode(params)}"
    return jsonify({
        'success': True,
        'auth_url': google_auth_url
    })


@auth_bp.route('/google/callback', methods=['GET', 'POST'])
def google_callback():
    """Handle Google OAuth callback"""
    try:
        code = request.args.get('code')
        if not code:
            return jsonify({'success': False, 'message': 'Authorization code not provided'}), 400

        # Exchange code for token
        token_url = 'https://oauth2.googleapis.com/token'
        token_data = {
            'client_id': os.getenv('GOOGLE_CLIENT_ID'),
            'client_secret': os.getenv('GOOGLE_CLIENT_SECRET'),
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': os.getenv('GOOGLE_REDIRECT_URI'),
        }

        token_response = requests.post(token_url, data=token_data)
        token_json = token_response.json()

        if 'access_token' not in token_json:
            return jsonify({'success': False, 'message': 'Failed to get access token'}), 400

        # Get user info from Google
        user_info_url = 'https://www.googleapis.com/oauth2/v2/userinfo'
        headers = {'Authorization': f'Bearer {token_json["access_token"]}'}
        user_response = requests.get(user_info_url, headers=headers)
        user_info = user_response.json()

        if 'email' not in user_info:
            return jsonify({'success': False, 'message': 'Failed to get user information'}), 400

        # Check if user exists
        existing_user = User.find_by_oauth('google', user_info['id'])
        
        if not existing_user:
            # Check if user exists with same email
            existing_user = User.find_by_email(user_info['email'])
            
        if existing_user:
            # Update OAuth info if needed
            if not existing_user.get('oauth_provider'):
                User.update_user(str(existing_user['_id']), {
                    'oauth_provider': 'google',
                    'oauth_id': user_info['id']
                })
                existing_user['oauth_provider'] = 'google'
                existing_user['oauth_id'] = user_info['id']
        else:
            # Create new user
            username = user_info['email'].split('@')[0]
            base_username = username
            counter = 1
            
            # Ensure username is unique
            while User.find_by_username(username):
                username = f"{base_username}{counter}"
                counter += 1

            new_user_data = {
                'name': user_info.get('name', user_info['email'].split('@')[0]),
                'email': user_info['email'],
                'username': username,
                'oauth_provider': 'google',
                'oauth_id': user_info['id'],
                'password': None  # No password for OAuth users
            }
            
            user_id = User.create_user(new_user_data)
            if user_id:
                existing_user = User.find_by_id(user_id)
                
                # Send welcome email
                try:
                    email_service.send_welcome_email(
                        user_info['email'], 
                        new_user_data['name']
                    )
                except Exception as e:
                    print(f"Failed to send welcome email: {e}")

        if existing_user:
            # Create JWT token
            access_token = create_access_token(identity=str(existing_user['_id']))
            
            # Redirect to frontend with token
            client_url = os.getenv('CLIENT_URL', 'http://localhost:5174')
            redirect_url = f"{client_url}/auth/callback?token={access_token}&user={existing_user['name']}"
            
            return redirect(redirect_url)
        else:
            client_url = os.getenv('CLIENT_URL', 'http://localhost:5174')
            redirect_url = f"{client_url}/auth/callback?error=registration_failed"
            return redirect(redirect_url)

    except Exception as e:
        print(f"Google OAuth error: {e}")
        client_url = os.getenv('CLIENT_URL', 'http://localhost:5174')
        redirect_url = f"{client_url}/auth/callback?error=oauth_failed"
        return redirect(redirect_url)


@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    user = User.find_by_id(user_id)

    if not user:
        return jsonify({'success': False, 'message': 'User not found'}), 404

    return jsonify({
        'success': True,
        'user': {
            'id': str(user['_id']),
            'name': user['name'],
            'email': user['email'],
            'username': user['username'],
            'phone': user.get('phone', ''),
            'dateOfBirth': user.get('dateOfBirth', ''),
            'location': user.get('location', ''),
            'bio': user.get('bio', ''),
            'emergencyContact': user.get('emergencyContact', {
                'name': '',
                'relationship': '',
                'phone': ''
            }),
            'oauth_provider': user.get('oauth_provider'),
            'created_at': user.get('created_at')
        }
    })


@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    current_password = data.get('current_password')
    new_password = data.get('new_password')
    
    if not all([current_password, new_password]):
        return jsonify({'success': False, 'message': 'Current and new password are required'}), 400
    
    user = User.find_by_id(user_id)
    if not user:
        return jsonify({'success': False, 'message': 'User not found'}), 404
    
    # Check if user has a password (OAuth users might not)
    if not user.get('password'):
        return jsonify({'success': False, 'message': 'Cannot change password for OAuth accounts'}), 400
    
    # Verify current password
    if not check_password_hash(user['password'], current_password):
        return jsonify({'success': False, 'message': 'Current password is incorrect'}), 400
    
    # Validate new password
    is_valid, message = validate_password(new_password)
    if not is_valid:
        return jsonify({'success': False, 'message': message}), 400
    
    # Update password
    hashed_password = generate_password_hash(new_password)
    if User.update_user(user_id, {'password': hashed_password}):
        return jsonify({
            'success': True,
            'message': 'Password changed successfully'
        })
    else:
        return jsonify({'success': False, 'message': 'Failed to update password'}), 500


@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()

        print(f"🔄 Profile update request for user_id: {user_id}")
        print(f"📦 Received data: {data}")

        # Fields that can be updated
        updatable_fields = ['name', 'phone', 'dateOfBirth', 'location', 'bio', 'emergencyContact']
        update_data = {}

        for field in updatable_fields:
            if field in data:
                update_data[field] = data[field]

        print(f"📝 Filtered update data: {update_data}")

        # Validate email if provided (email should not be updatable for now)
        if 'email' in data:
            print("❌ Email update attempted - not allowed")
            return jsonify({'success': False, 'message': 'Email cannot be updated'}), 400

        if not update_data:
            print("❌ No valid fields to update")
            return jsonify({'success': False, 'message': 'No valid fields to update'}), 400

        # Attempt to update user
        print(f"🔄 Calling User.update_user with user_id: {user_id}")
        update_result = User.update_user(user_id, update_data)
        print(f"📊 Update result: {update_result}")

        if update_result:
            # Get updated user data
            user = User.find_by_id(user_id)
            print(f"✅ Profile updated successfully for user: {user_id}")
            return jsonify({
                'success': True,
                'message': 'Profile updated successfully',
                'user': {
                    'id': str(user['_id']),
                    'name': user['name'],
                    'email': user['email'],
                    'username': user['username'],
                    'phone': user.get('phone'),
                    'dateOfBirth': user.get('dateOfBirth'),
                    'location': user.get('location'),
                    'bio': user.get('bio'),
                    'emergencyContact': user.get('emergencyContact'),
                    'created_at': user.get('created_at')
                }
            })
        else:
            print(f"❌ Failed to update profile for user: {user_id}")
            return jsonify({'success': False, 'message': 'Failed to update profile'}), 500

    except Exception as e:
        print(f"💥 Exception in update_profile: {str(e)}")
        print(f"💥 Exception type: {type(e)}")
        import traceback
        print(f"💥 Traceback: {traceback.format_exc()}")
        return jsonify({'success': False, 'message': f'Internal server error: {str(e)}'}), 500


@auth_bp.route('/profile/stats', methods=['GET'])
@jwt_required()
def get_profile_stats():
    """Get user profile statistics for the dashboard"""
    user_id = get_jwt_identity()
    
    # For now, return mock stats. In a real implementation, 
    # you would calculate these from user's actual data
    stats = {
        'daysActive': 15,
        'goalsCompleted': 8,
        'moodStreak': 7,
        'sessions': 12
    }
    
    return jsonify({
        'success': True,
        'stats': stats
    })
