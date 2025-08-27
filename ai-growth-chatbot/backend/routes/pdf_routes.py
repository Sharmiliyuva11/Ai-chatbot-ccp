from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
import os

from services.pdf_service import extract_pdf_text, generate_pdf_questions, explain_pdf

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), '..', 'uploads')
os.makedirs(UPLOAD_DIR, exist_ok=True)

pdf_routes = Blueprint('pdf', __name__)
pdf_bp = pdf_routes  # Alias for compatibility with app.py import

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
    file.save(save_path)

    return jsonify({"success": True, "filename": file.filename, "path": save_path})


# =========================
# 📌 Read & Summarize / Explain PDF
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
        return jsonify({"success": False, "message": "Could not extract text"}), 400

    result = explain_pdf(text)
    # result is a dict with keys: success, reply or error
    if result.get('success') and result.get('reply'):
        return jsonify({"success": True, "summary": result['reply']})
    else:
        return jsonify({"success": False, "message": result.get('error', 'Failed to summarize/explain PDF')})


# =========================
# 📌 Generate Questions from PDF
# =========================
@pdf_routes.route('/questions', methods=['POST'])
@jwt_required()
def generate_questions():
    data = request.get_json() or {}
    pdf_path = data.get("path")

    if not pdf_path or not os.path.exists(pdf_path):
        return jsonify({"success": False, "message": "Invalid or missing PDF path"}), 400

    text = extract_pdf_text(pdf_path)
    if not text:
        return jsonify({"success": False, "message": "Could not extract text"}), 400

    result = generate_pdf_questions(text)
    if result.get('success') and result.get('reply'):
        return jsonify({"success": True, "questions": result['reply']})
    else:
        return jsonify({"success": False, "message": result.get('error', 'Failed to generate questions from PDF')})
