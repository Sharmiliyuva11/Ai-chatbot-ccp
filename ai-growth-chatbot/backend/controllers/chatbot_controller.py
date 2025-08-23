from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
import os
import subprocess
import uuid
from dotenv import load_dotenv

from services.openai_services import generate_openai_response
from services.groq_service import generate_groq_response
from services.grammar_services import evaluate_speech_grammar
from services.sentiment_service import analyze_sentiment

# File handling directory
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), '..', 'uploads')
os.makedirs(UPLOAD_DIR, exist_ok=True)

load_dotenv()

# Blueprint for chatbot routes
chatbot_bp = Blueprint('chatbot', __name__)

# Default system prompt
DEFAULT_SYSTEM_PROMPT = (
    "You are a supportive AI assistant designed for college students. "
    "You help with coding doubts, provide communication and grammar feedback, "
    "and offer mental wellness advice when someone is feeling low or unmotivated."
)

# ===================================
# 📌 Route: Handle Chat Messages
# ===================================
@chatbot_bp.route('/message', methods=['POST'])
@jwt_required()
def handle_chat():
    data = request.get_json(silent=True) or {}
    message = (data.get('message') or '').strip()

    if not message:
        return jsonify({'success': False, 'message': 'No message provided'}), 400

    # Decide AI provider per-request to reflect current env/state
    provider = (os.getenv("AI_PROVIDER", "groq") or "groq").lower()

    if provider == "groq":
        result = generate_groq_response(
            user_message=message,
            system_prompt=DEFAULT_SYSTEM_PROMPT
        )
    else:
        result = generate_openai_response(
            user_message=message,
            system_prompt=DEFAULT_SYSTEM_PROMPT
        )

    if result.get("success"):
        return jsonify({'success': True, 'response': result.get("reply", "")})
    else:
        return jsonify({'success': False, 'message': result.get("error", "Unknown error")}), 200


# ===========================================
# 📌 Route: Evaluate Grammar from Voice File
# ===========================================
@chatbot_bp.route('/grammar/evaluate', methods=['POST'])
@jwt_required()
def evaluate_grammar():
    audio = request.files.get('audio')
    if not audio:
        return jsonify({"success": False, "message": "No audio file provided"}), 400

    # Save uploaded file with original extension
    ext = os.path.splitext(audio.filename or "")[1].lower() or ".webm"
    temp_id = uuid.uuid4().hex
    raw_path = os.path.join(UPLOAD_DIR, f"upload_{temp_id}{ext}")
    audio.save(raw_path)

    # Ensure WAV format for speech_recognition
    wav_path = os.path.join(UPLOAD_DIR, f"upload_{temp_id}.wav")

    try:
        if ext not in [".wav", ".aiff", ".aif", ".flac"]:
            # Try to convert using ffmpeg if available
            try:
                subprocess.run([
                    "ffmpeg", "-y", "-i", raw_path, "-ac", "1", "-ar", "16000", wav_path
                ], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except Exception as conv_err:
                # If conversion fails, return a clear message
                return jsonify({
                    "success": False,
                    "message": "Audio file could not be read as PCM WAV/AIFF/FLAC. Please install ffmpeg or upload a WAV/AIFF/FLAC file.",
                    "detail": str(conv_err)
                }), 200
        else:
            wav_path = raw_path

        result = evaluate_speech_grammar(wav_path)
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "message": f"Grammar eval error: {str(e)}"}), 200
    finally:
        # Cleanup temp files
        try:
            if os.path.exists(raw_path):
                os.remove(raw_path)
        except Exception:
            pass
        try:
            if os.path.exists(wav_path) and wav_path != raw_path:
                os.remove(wav_path)
        except Exception:
            pass


# ======================================
# 📌 Route: Generic File Upload
# ======================================
@chatbot_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_file():
    file = request.files.get('file')
    if not file:
        return jsonify({"success": False, "message": "No file provided"}), 400

    save_path = os.path.join(UPLOAD_DIR, file.filename)
    try:
        file.save(save_path)
        return jsonify({"success": True, "filename": file.filename, "path": save_path})
    except Exception as e:
        return jsonify({"success": False, "message": f"Upload error: {str(e)}"}), 200


# ======================================
# 📌 Route: Analyze Sentiment of Text
# ======================================
@chatbot_bp.route('/sentiment', methods=['POST'])
@jwt_required()
def analyze_sentiment_route():
    data = request.get_json(silent=True) or {}
    message = (data.get('message') or '').strip()

    if not message:
        return jsonify({'success': False, 'message': 'No message provided'}), 400

    try:
        result = analyze_sentiment(message)
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "message": f"Sentiment error: {str(e)}"}), 200
