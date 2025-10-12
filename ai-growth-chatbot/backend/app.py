from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

# SocketIO
from flask_socketio import SocketIO

# ===============================
# 🔹 Load Environment Variables
# ===============================
load_dotenv()

# ===============================
# 🔹 Import Blueprints
# ===============================
from routes.auth_routes import auth_routes
from routes.chatbot_routes import chatbot_routes
from routes.reminder_routes import reminder_routes
from routes.mood_routes import mood_routes
from routes.analytics_routes import analytics_routes

from routes.mindspace_routes import mindspace_bp
from routes.pdf_routes import pdf_bp   # ✅ Updated (was pdf_routes before)
from routes.roundtable_routes import roundtable_bp
from routes.coding_routes import coding_bp
from routes.local_support_routes import local_support_bp

# Initialize OAuth after app creation
from controllers.auth_controller import init_oauth

# ===============================
# 🔹 Create Flask App
# ===============================
app = Flask(__name__)

# ===============================
# 🔹 CORS Configuration
# ===============================
# Allow common local dev frontend ports and any explicitly set CLIENT_URL.
# This helps when Vite or other dev servers choose a different port (e.g. 5175).
dev_ports = [5173, 5174, 5175, 5176, 5177, 5178, 5179]
client_urls = []
for p in dev_ports:
    client_urls.append(f"http://localhost:{p}")
    client_urls.append(f"http://127.0.0.1:{p}")
# include any explicit CLIENT_URL from env (keeps existing behavior)
env_client = os.getenv('CLIENT_URL')
if env_client:
    client_urls.append(env_client)

# Enable CORS for API endpoints explicitly, allow common methods and headers
# (Content-Type, Authorization) so preflight (OPTIONS) requests succeed.
from flask_cors import CORS as _CORS

_CORS(app,
    # Allow CORS for all paths during local development so probes to '/'
    # and other non-/api routes succeed. In production, restrict this.
    resources={r"/*": {"origins": client_urls}},
    supports_credentials=True,
    allow_headers=["Content-Type", "Authorization"],
    methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]
)

# ===============================
# 🔹 Session Configuration (OAuth)
# ===============================
app.config['SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-default-secret-key')
app.config['SESSION_COOKIE_SECURE'] = False  # ⚠️ Set True in production (HTTPS only)
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# ===============================
# 🔹 JWT Configuration
# ===============================
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-default-secret-key')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False  # Tokens don’t expire for now
jwt = JWTManager(app)

# Initialize SocketIO (allow CORS from frontend)
# Use 'threading' async mode to avoid eventlet/dnspython greendns issues on some environments
socketio = SocketIO(app, cors_allowed_origins=client_urls, async_mode='threading')

# ===============================
# 🔹 Initialize OAuth
# ===============================
init_oauth(app)

# ===============================
# 🔹 Register Blueprints
# ===============================

app.register_blueprint(auth_routes, url_prefix="/api/auth")
app.register_blueprint(chatbot_routes, url_prefix="/api/chatbot")
app.register_blueprint(reminder_routes, url_prefix="/api/reminder")
app.register_blueprint(mood_routes, url_prefix="/api/mood")
app.register_blueprint(analytics_routes, url_prefix="/api/analytics")
app.register_blueprint(mindspace_bp, url_prefix="/api/mindspace")
app.register_blueprint(pdf_bp, url_prefix="/api/pdf")   # ✅ Fixed name
app.register_blueprint(roundtable_bp, url_prefix="/api/roundtable")
app.register_blueprint(coding_bp, url_prefix="/api/coding")
app.register_blueprint(local_support_bp, url_prefix="/api/local-support")

# Import socket event handlers so they are registered
try:
    import routes.socket_events  # noqa: F401
except Exception:
    pass

# ===============================
# 🔹 Health Check Route
# ===============================
@app.route("/")
def home():
    return {"message": "🚀 AI Chatbot Backend is running ✅"}

# ===============================
# 🔹 Run App
# ===============================
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    # Use socketio.run to enable websocket support
    socketio.run(app, debug=True, port=port, host="0.0.0.0")
