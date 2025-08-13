# routes/backend/auth_routes.py
from controllers.auth_controller import auth_bp

# Use the blueprint directly from the controller
auth_routes = auth_bp
