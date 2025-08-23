import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Default system prompt for the assistant
DEFAULT_SYSTEM_PROMPT = (
    "You are a helpful, intelligent assistant that helps college students "
    "with coding questions, grammar and fluency improvement, and mental wellness support."
)

# Lazily create client only when needed
_client = None

def _get_client():
    global _client
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    if _client is None:
        _client = OpenAI(api_key=api_key)
    return _client


def generate_openai_response(
    user_message,
    system_prompt=DEFAULT_SYSTEM_PROMPT,
    model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
    max_tokens=500,
):
    """Call OpenAI to generate a response. Returns a dict with success flag.

    Provides safer defaults and clearer error messages to avoid 500s bubbling up.
    """
    client = _get_client()
    if client is None:
        return {
            "success": False,
            "error": "Missing OPENAI_API_KEY. Set it in your backend .env and restart the server.",
        }

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            temperature=0.7,
            max_tokens=max_tokens,
        )

        reply = response.choices[0].message.content
        return {"success": True, "reply": (reply or "").strip()}

    except Exception as e:
        # Surface a concise error message back to the controller
        return {"success": False, "error": f"OpenAI error: {str(e)}"}
