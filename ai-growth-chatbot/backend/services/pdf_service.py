import os
import re
import PyPDF2
from dotenv import load_dotenv

from services.groq_service import generate_groq_response

load_dotenv()


# Extract text from PDF
def extract_pdf_text(pdf_path):
    """Extract text from a PDF file using PyPDF2"""
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
    """Generate an explanation/summary of PDF content"""
    prompt = f"Explain the following study material in simple terms for students:\n\n{text[:4000]}"
    
    try:
        return generate_groq_response(prompt)
    except Exception as e:
        return {"success": False, "error": f"Failed to explain PDF content: {str(e)}"}


# Generate Questions from PDF content
def generate_pdf_questions(text):
    """Generate multiple-choice questions from PDF content"""
    prompt = f"""
    Based on the following study material, generate 10 multiple-choice questions 
    with 4 options each and also mark the correct answer clearly:
    
    {text[:4000]}
    """
    
    try:
        return generate_groq_response(prompt)
    except Exception as e:
        return {"success": False, "error": f"Failed to generate questions: {str(e)}"}


# Flexible answer generator from PDF content
def answer_from_pdf(text, user_query):
    """Generate answers from PDF based on user query - supports MCQ, mark-based, and general queries"""
    # Lowercase for intent detection
    q = user_query.lower()
    
    # MCQ intent
    if 'mcq' in q or 'multiple choice' in q:
        prompt = f"""
        Based on the following study material, generate 10 multiple-choice questions 
        with 4 options each and also mark the correct answer clearly:
        
        {text[:4000]}
        """
        try:
            return generate_groq_response(prompt)
        except Exception as e:
            return {"success": False, "error": f"Failed to generate MCQs: {str(e)}"}
    
    # Mark-based intent
    mark_match = re.search(r'(\d+)\s*(m|mark)', q)
    if mark_match:
        marks = mark_match.group(1)
        prompt = f"""
        Based on the following study material, write a detailed answer suitable for a {marks}-mark question.
        The answer should be clear, relevant, and match the expected length and depth for a {marks}-mark answer in an exam.

        Question: {user_query}

        Material:
        {text[:4000]}
        """
        try:
            return generate_groq_response(prompt)
        except Exception as e:
            return {"success": False, "error": f"Failed to generate {marks}-mark answer: {str(e)}"}
    
    # Default: explain/answer the question
    prompt = f"""
    Based on the following study material, answer the user's question:
    
    Question: {user_query}
    
    Material:
    {text[:4000]}
    """
    try:
        return generate_groq_response(prompt)
    except Exception as e:
        return {"success": False, "error": f"Failed to generate answer: {str(e)}"}