import os
import json
from dotenv import load_dotenv
from groq import Groq
from groq import GroqError

load_dotenv()

DEFAULT_GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

# Lazily create Groq client only when needed
_client = None

def _get_client():
    global _client
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or api_key == "your_groq_api_key_here":
        return None
    if _client is None:
        try:
            _client = Groq(api_key=api_key)
        except GroqError as e:
            print(f"Groq client initialization error: {e}")
            return None
    return _client

DEFAULT_SYSTEM_PROMPT = (
    "You are a supportive AI assistant designed for college students. "
    "You help with coding doubts, grammar and fluency, and mental wellness."
)

def generate_groq_response(user_message, system_prompt=DEFAULT_SYSTEM_PROMPT):
    client = _get_client()
    if client is None:
        return {"success": False, "error": "Missing or invalid GROQ_API_KEY. Please set a valid API key in the backend/.env file and restart the server."}
    try:
        response = client.chat.completions.create(
            model=DEFAULT_GROQ_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            temperature=0.7,
            max_tokens=500,
        )
        reply = response.choices[0].message.content.strip()
        return {"success": True, "reply": reply}
    except GroqError as e:
        if "401" in str(e) or "Invalid API Key" in str(e):
            return {"success": False, "error": "Invalid GROQ_API_KEY. Please check your API key in the backend/.env file."}
        else:
            return {"success": False, "error": f"Groq API error: {str(e)}"}
    except Exception as e:
        return {"success": False, "error": f"Unexpected error: {str(e)}"}
