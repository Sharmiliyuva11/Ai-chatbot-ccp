from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

# Route Blueprints
from routes.auth_routes import auth_routes
from routes.chatbot_routes import chatbot_routes
from routes.reminder_routes import reminder_routes
from routes.mindspace_routes import mindspace_bp  # ✅ NEW

# Initialize OAuth after app creation
from controllers.auth_controller import init_oauth

load_dotenv()

app = Flask(__name__)

# CORS Configuration - Allow credentials for OAuth
CORS(app, supports_credentials=True, origins=[
    "http://localhost:5174",
    "http://127.0.0.1:5174",
    os.getenv('CLIENT_URL', 'http://localhost:5174')
])

# Session Configuration (required for OAuth)
app.config['SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-default-secret-key')
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# JWT Configuration
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-default-secret-key')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False  # Tokens don't expire
jwt = JWTManager(app)

# Initialize OAuth
init_oauth(app)

# Register route blueprints
app.register_blueprint(auth_routes, url_prefix="/api/auth")
app.register_blueprint(chatbot_routes, url_prefix="/api/chatbot")
app.register_blueprint(reminder_routes, url_prefix="/api/reminder")
app.register_blueprint(mindspace_bp, url_prefix="/api/mindspace")  # ✅ NEW

@app.route("/")
def home():
    return {"message": "AI Chatbot Backend is running ✅"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(debug=True, port=port, host='0.0.0.0')
