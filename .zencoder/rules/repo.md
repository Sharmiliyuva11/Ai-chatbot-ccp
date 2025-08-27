# AI Chatbot (CCP) — Repository Overview

## Project Structure
- backend: Flask API with JWT auth, chat, sentiment, grammar
  - app.py: Flask app bootstrap and blueprints
  - controllers: request handling (auth, chatbot, mindspace, reminders)
  - routes: blueprint bindings
  - services: integrations (OpenAI/Groq, grammar, email, sentiment)
  - models: DB models (Mongo via pymongo)
  - uploads: temp files (audio)
  - .env: backend configuration
- frontend: React (Vite) client
  - src/components/Chatbot: chat UI + voice recording
  - src/services/api.js: API wrapper (uses http://localhost:5000/api)

## Environment (.env in backend)
- Database
  - MONGO_URI
- Auth & App
  - JWT_SECRET_KEY
  - PORT (default 5000)
  - CLIENT_URL (e.g., http://localhost:5174)
- Email
  - EMAIL_HOST, EMAIL_PORT, EMAIL_USER, EMAIL_PASS
- Google OAuth
  - GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REDIRECT_URI
- AI Provider Switch
  - AI_PROVIDER=groq | openai
  - Groq: GROQ_API_KEY, GROQ_MODEL (e.g., llama3-70b-8192)
  - OpenAI: OPENAI_API_KEY, OPENAI_MODEL (default gpt-4o-mini)

## AI Provider Integration
- Selection: controllers/chatbot_controller.py reads AI_PROVIDER and routes to:
  - services/groq_service.py → Groq client (groq package)
  - services/openai_services.py → OpenAI client (openai package)
- To use Groq: set AI_PROVIDER=groq and provide GROQ_API_KEY. Restart backend.

## Voice Grammar Flow
- Frontend records audio as WebM (Opus) using MediaRecorder
- Backend route /api/chatbot/grammar/evaluate saves the upload and, if needed, converts to 16kHz mono WAV using ffmpeg, then processes with speech_recognition + language_tool_python
- Requirement: ffmpeg must be installed and available in PATH on the backend host

## Running Locally
1. Backend
   - Python 3.9+
   - cd ai-growth-chatbot/backend
   - Create .env (see above)
   - python -m venv venv && venv\\Scripts\\activate
   - pip install -r requirements.txt
   - python app.py (default http://localhost:5000)
2. Frontend
   - cd ai-growth-chatbot/frontend
   - npm install
   - npm run dev (default http://localhost:5174)

## Important Endpoints (prefix /api)
- Auth: /auth/register, /auth/login, /auth/profile, /auth/forgot-password, /auth/reset-password
- Google OAuth: /auth/google, /auth/google/callback
- Chatbot: /chatbot/message, /chatbot/grammar/evaluate, /chatbot/upload, /chatbot/sentiment
- MindSpace: /mindspace/*

## Common Issues
- Invalid API Key (OpenAI): Appears if AI_PROVIDER=openai with bad OPENAI_API_KEY. Fix by switching AI_PROVIDER=groq and setting GROQ_API_KEY, or correct OPENAI_API_KEY.
- Grammar eval error (audio format): Install ffmpeg or upload WAV/AIFF/FLAC.

## Notes
- Keep secrets out of version control. Rotate any keys committed by mistake and use a separate .env.
- Frontend API base URL is set in frontend/src/services/api.js.