import os
import re
import PyPDF2
from dotenv import load_dotenv

from services.groq_service import generate_groq_response
from services.openai_services import generate_openai_response

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
        return _call_ai_provider(prompt)
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
        return _call_ai_provider(prompt)
    except Exception as e:
        return {"success": False, "error": f"Failed to generate questions: {str(e)}"}


def _call_ai_provider(prompt: str):
    """Route prompt to the configured AI provider and normalize response."""
    provider = (os.getenv("AI_PROVIDER", "groq") or "groq").lower()

    if provider == "groq":
        return generate_groq_response(prompt)

    return generate_openai_response(prompt)


# Flexible answer generator from PDF content
def answer_from_pdf(text, user_query):
    """Generate answers from PDF based on user query - supports MCQ, mark-based, and general queries"""
    q = user_query.lower()

    # Mark-based intent (prioritize over MCQ)
    mark_match = re.search(r"(\d+)\s*(m|mark)", q)
    if mark_match:
        marks = mark_match.group(1)
        content_length = min(8000 if int(marks) >= 10 else 4000, len(text))
        content = text[:content_length]

        if any(keyword in q for keyword in ["question", "questions", "generate", "give", "create", "provide"]):
            if int(marks) >= 10:
                prompt = f"""
                Based on the following comprehensive study material, generate a {marks}-mark question suitable for university-level examination.

                Requirements for {marks}-mark question:
                - Create 1 comprehensive question that requires in-depth analysis and understanding
                - The question should test multiple concepts and require detailed explanations
                - Include sub-questions (a, b, c) if appropriate
                - Ensure the question demands critical thinking and application of concepts
                - Question should be answerable within {int(marks) * 2 - 3} minutes of writing time
                - Focus on important topics like Express.js features, routing, middleware, error handling, etc.

                Study Material:
                {content}

                Format your response as:
                **{marks}-Mark Question:**
                [Your comprehensive question here]

                **Expected Answer Coverage:**
                [Brief outline of what a complete answer should include]
                """
            else:
                prompt = f"""
                Based on the following study material, generate {marks}-mark questions.
                Create detailed questions that would be appropriate for a {marks}-mark answer in an exam.
                Provide clear, well-structured questions that test understanding of the material.

                Material:
                {content}
                """
        else:
            prompt = f"""
            Based on the following study material, write a detailed answer suitable for a {marks}-mark question.
            The answer should be clear, relevant, and match the expected length and depth for a {marks}-mark answer in an exam.

            Question: {user_query}

            Material:
            {content}
            """

        try:
            return _call_ai_provider(prompt)
        except Exception as e:
            return {"success": False, "error": f"Failed to generate {marks}-mark content: {str(e)}"}

    if "mcq" in q or "multiple choice" in q:
        prompt = f"""
        Based on the following study material, generate 10 multiple-choice questions
        with 4 options each and also mark the correct answer clearly:

        {text[:6000]}
        """
        try:
            return _call_ai_provider(prompt)
        except Exception as e:
            return {"success": False, "error": f"Failed to generate MCQs: {str(e)}"}

    prompt = f"""
    Based on the following study material, answer the user's question:

    Question: {user_query}

    Material:
    {text[:6000]}
    """
    try:
        return _call_ai_provider(prompt)
    except Exception as e:
        return {"success": False, "error": f"Failed to generate answer: {str(e)}"}