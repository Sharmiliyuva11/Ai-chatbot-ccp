import os
import PyPDF2
from dotenv import load_dotenv

from services.groq_service import generate_groq_response
from services.openai_services import generate_openai_response

load_dotenv()

# Extract text from PDF
def extract_pdf_text(pdf_path):
    text = ""
    try:
        with open(pdf_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""
    except Exception as e:
        return f"Error extracting PDF: {e}"
    return text.strip()


# Summarize / Explain PDF content
def explain_pdf(text):
    prompt = f"Explain the following study material in simple terms for students:\n\n{text[:4000]}"

    # Prefer Groq, fallback to OpenAI
    try:
        return generate_groq_response(prompt)
    except Exception:
        return generate_openai_response(prompt)


# Generate Questions from PDF content
def generate_pdf_questions(text):
    prompt = f"""
    Based on the following study material, generate 10 multiple-choice questions 
    with 4 options each and also mark the correct answer clearly:
    
    {text[:4000]}
    """

    # Prefer Groq, fallback to OpenAI
    try:
        return generate_groq_response(prompt)
    except Exception:
        return generate_openai_response(prompt)

import PyPDF2
import os

def extract_text_from_pdf(pdf_path):
    try:
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
        return {"success": True, "text": text.strip()}
    except Exception as e:
        return {"success": False, "error": str(e)}
