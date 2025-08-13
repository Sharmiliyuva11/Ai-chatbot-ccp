from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
from dotenv import load_dotenv

from services.openai_services import generate_openai_response
from services.grammar_services import evaluate_speech_grammar
from services.sentiment_service import analyze_sentiment

load_dotenv()

# Blueprint for chatbot routes
chatbot_bp = Blueprint('chatbot', __name__)

# Default system prompt for OpenAI
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
    data = request.get_json()
    message = data.get('message')

    if not message:
        return jsonify({'success': False, 'message': 'No message provided'}), 400

    result = generate_openai_response(
        user_message=message,
        system_prompt=DEFAULT_SYSTEM_PROMPT
    )

    if result["success"]:
        return jsonify({'success': True, 'response': result["reply"]})
    else:
        return jsonify({'success': False, 'error': result["error"]}), 500


# ===========================================
# 📌 Route: Evaluate Grammar from Voice File
# ===========================================
@chatbot_bp.route('/grammar/evaluate', methods=['POST'])
@jwt_required()
def evaluate_grammar():
    audio = request.files.get('audio')
    if not audio:
        return jsonify({"success": False, "message": "No audio file provided"}), 400

    audio_path = "temp_audio.wav"
    audio.save(audio_path)

    try:
        result = evaluate_speech_grammar(audio_path)
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ======================================
# 📌 Route: Analyze Sentiment of Text
# ======================================
@chatbot_bp.route('/sentiment', methods=['POST'])
@jwt_required()
def analyze_sentiment_route():
    data = request.get_json()
    message = data.get('message')

    if not message:
        return jsonify({'success': False, 'message': 'No message provided'}), 400

    try:
        result = analyze_sentiment(message)
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
