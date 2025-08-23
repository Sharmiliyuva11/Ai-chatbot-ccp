# 📘 Project Best Practices

## 1. Project Purpose  
Cally (AI Growth Chatbot) is a comprehensive AI-powered platform that combines mental health support, coding tools, and community features. It aims to help users (especially students and professionals) thrive in both personal and professional growth by providing an integrated environment for wellness, learning, and collaboration.

## 2. Project Structure
- **Monorepo Layout:**
  - `ai-growth-chatbot/`
    - `frontend/`: React 19 app (Vite, React Router) for the user interface
    - `backend/`: Flask REST API for authentication, chatbot, reminders, and mindspace features
- **Frontend:**
  - `src/pages/`: Feature-based page components (Dashboard, CodingSpace, MindSpace, etc.)
  - `src/components/`: Shared UI components (Sidebar, Layout, Chatbot, etc.)
  - `src/services/`: API abstraction for backend communication
- **Backend:**
  - `controllers/`: Route handler logic (auth, chatbot, reminders, mindspace)
  - `routes/`: Flask blueprints for API endpoints
  - `models/`: Data access and business logic (MongoDB, in-memory fallback)
  - `services/`: Integrations (OpenAI, grammar, sentiment, email)
  - `config.py`: Loads environment variables and config
  - `.env`: Secrets (Mongo URI, JWT, OpenAI keys)

## 3. Test Strategy
- **Current State:** No formal automated tests found in the codebase.
- **Recommendations:**
  - Use `pytest` for backend unit/integration tests (mock MongoDB, test controllers/services)
  - Use `Jest` and `React Testing Library` for frontend (test components, API integration)
  - Place backend tests in `backend/tests/` and frontend tests in `frontend/src/__tests__/`
  - Use descriptive test names and group by feature
  - Mock external APIs (OpenAI, email, etc.)
  - Aim for high coverage on business logic and critical flows

## 4. Code Style
- **Backend (Python):**
  - Follows PEP8 (indentation, snake_case for functions/vars, PascalCase for classes)
  - Uses type hints sparingly; recommend adding for clarity
  - Docstrings for public methods/classes are encouraged
  - Error handling: Returns JSON with `success` and `message`; uses HTTP status codes
  - Environment/config via `os.getenv` and `.env` files
- **Frontend (React/JSX):**
  - Functional components, hooks (useState, useEffect)
  - File and component names: PascalCase for components, camelCase for functions/vars
  - CSS modules or feature-based CSS files
  - API calls abstracted in `services/api.js`
  - Comments for complex logic; prop types or TypeScript recommended for large components
  - Error handling: User feedback via alerts or UI messages

## 5. Common Patterns
- **Backend:**
  - Blueprint pattern for Flask route modularity
  - Service layer for external integrations (OpenAI, grammar, sentiment)
  - In-memory fallback for MongoDB (for local/dev/testing)
  - JWT-based authentication (Flask-JWT-Extended)
- **Frontend:**
  - ProtectedRoute/PublicRoute for auth-based navigation
  - Centralized API service for backend communication
  - Feature-based folder structure for scalability
  - Reusable UI components (Sidebar, Layout, etc.)

## 6. Do's and Don'ts
- ✅ Use environment variables for secrets and config
- ✅ Keep business logic in services/models, not controllers/routes
- ✅ Use blueprints for new API modules
- ✅ Write clear, user-friendly error messages
- ✅ Use protected routes for sensitive pages
- ✅ Keep UI state in React hooks, not global unless necessary
- ✅ Use version control and commit often
- ❌ Do not hardcode secrets or credentials in code
- ❌ Do not mix business logic with route/controller code
- ❌ Do not expose stack traces or sensitive info in API errors
- ❌ Do not bypass authentication for protected endpoints
- ❌ Do not use direct DOM manipulation in React

## 7. Tools & Dependencies
- **Frontend:**
  - React 19, React Router, Vite, Lucide React (icons), ESLint
- **Backend:**
  - Flask, Flask-CORS, Flask-JWT-Extended, PyMongo, python-dotenv, OpenAI, language_tool_python, textblob
- **Setup:**
  - Frontend: `npm install && npm run dev` in `frontend/`
  - Backend: `pip install -r requirements.txt` in `backend/`
  - Set up `.env` with Mongo URI, JWT secret, OpenAI key

## 8. Other Notes
- The backend supports both persistent (MongoDB) and in-memory storage (for dev/testing)
- API endpoints are versioned under `/api/`
- All authentication is JWT-based; tokens are stored in localStorage on the frontend
- The project is designed for extensibility: add new features as new pages/components (frontend) and blueprints/services (backend)
- When generating new code, follow the feature-based structure and keep logic modular and testable
- MindSpace, CodingSpace, and other features are intended to be extensible modules
