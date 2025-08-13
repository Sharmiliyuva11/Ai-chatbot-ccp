from flask import Blueprint, request, jsonify
from services.sentiment_service import analyze_sentiment
from flask_jwt_extended import jwt_required, get_jwt_identity

mindspace_bp = Blueprint("mindspace", __name__)

@mindspace_bp.route("/api/mindspace/mood", methods=["POST"])
@jwt_required()
def analyze_mood():
    data = request.get_json()
    stars = data.get("stars")
    user_text = data.get("text", "")

    if stars is None:
        return jsonify({"success": False, "message": "Mood rating (stars) is required"}), 400

    # Analyze only if mood is 1–2 stars or user provides a text
    if stars <= 2 or user_text:
        sentiment_result = analyze_sentiment(user_text or "I'm not feeling great.")
        return jsonify({
            "success": True,
            "sentiment": sentiment_result["sentiment"],
            "suggestion": sentiment_result["suggestion"]
        })

    return jsonify({"success": True, "message": "Glad you're feeling okay! 😊"})
