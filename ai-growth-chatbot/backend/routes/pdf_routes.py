from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
import os

from services.pdf_service import extract_pdf_text, generate_pdf_questions, explain_pdf, answer_from_pdf

# Create Blueprint
pdf_routes = Blueprint('pdf', __name__)
pdf_bp = pdf_routes  # Alias for compatibility with app.py import

# Upload directory
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), '..', 'uploads')
os.makedirs(UPLOAD_DIR, exist_ok=True)


# =========================
# 📌 Upload PDF
# =========================
@pdf_routes.route('/upload', methods=['POST'])
@jwt_required()
def upload_pdf():
    file = request.files.get('file')
    if not file:
        return jsonify({"success": False, "message": "No file provided"}), 400

    save_path = os.path.join(UPLOAD_DIR, file.filename)
    try:
        file.save(save_path)
        return jsonify({"success": True, "filename": file.filename, "path": save_path})
    except Exception as e:
        return jsonify({"success": False, "message": f"Upload error: {str(e)}"}), 400


# =========================
# 📌 Generate Questions from PDF
# =========================
@pdf_routes.route('/questions', methods=['POST'])
@jwt_required()
def get_pdf_questions():
    data = request.get_json() or {}
    pdf_path = data.get("path")

    if not pdf_path or not os.path.exists(pdf_path):
        return jsonify({"success": False, "message": "Invalid or missing PDF path"}), 400

    text = extract_pdf_text(pdf_path)
    if not text:
        return jsonify({"success": False, "message": "Could not extract text from PDF"}), 400

    result = generate_pdf_questions(text)
    if result.get('success') and result.get('reply'):
        return jsonify({"success": True, "questions": result['reply']})
    else:
        return jsonify({"success": False, "message": result.get('error', 'Failed to generate questions from PDF')})


# =========================
# 📌 Explain/Summarize PDF
# =========================
@pdf_routes.route('/explain', methods=['POST'])
@jwt_required()
def explain():
    data = request.get_json() or {}
    pdf_path = data.get("path")

    if not pdf_path or not os.path.exists(pdf_path):
        return jsonify({"success": False, "message": "Invalid or missing PDF path"}), 400

    text = extract_pdf_text(pdf_path)
    if not text:
        return jsonify({"success": False, "message": "Could not extract text from PDF"}), 400

    result = explain_pdf(text)
    if result.get('success') and result.get('reply'):
        return jsonify({"success": True, "explanation": result['reply']})
    else:
        return jsonify({"success": False, "message": result.get('error', 'Failed to explain PDF content')})


# =========================
# 📌 Answer Questions from PDF (MCQ, Mark-based, or General)
# =========================
@pdf_routes.route('/answer', methods=['POST'])
@jwt_required()
def answer_pdf():
    data = request.get_json() or {}
    pdf_path = data.get("path")
    user_query = data.get("query")

    if not pdf_path or not os.path.exists(pdf_path):
        return jsonify({"success": False, "message": "Invalid or missing PDF path"}), 400
    if not user_query:
        return jsonify({"success": False, "message": "Missing user query"}), 400

    text = extract_pdf_text(pdf_path)
    if not text:
        return jsonify({"success": False, "message": "Could not extract text from PDF"}), 400

    result = answer_from_pdf(text, user_query)
    if result.get('success') and result.get('reply'):
        return jsonify({"success": True, "answer": result['reply']})
    else:
        return jsonify({"success": False, "message": result.get('error', 'Failed to generate answer from PDF')})


# =========================
# 📌 Debug: View Extracted PDF Text
# =========================
@pdf_routes.route('/debug/pdf-text', methods=['POST'])
@jwt_required()
def debug_pdf_text():
    data = request.get_json() or {}
    pdf_path = data.get("path")
    
    if not pdf_path or not os.path.exists(pdf_path):
        return jsonify({"success": False, "message": "Invalid or missing PDF path"}), 400
    
    text = extract_pdf_text(pdf_path)
    print("[DEBUG] Extracted PDF text (first 500 chars):", text[:500])
    return jsonify({"success": True, "text": text[:500], "length": len(text)})