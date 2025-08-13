import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Default system prompt for the assistant
DEFAULT_SYSTEM_PROMPT = (
    "You are a helpful, intelligent assistant that helps college students "
    "with coding questions, grammar and fluency improvement, and mental wellness support."
)

def generate_openai_response(user_message, system_prompt=DEFAULT_SYSTEM_PROMPT, model="gpt-3.5-turbo", max_tokens=500):
    """
    Calls OpenAI API to generate a response based on user input.
    
    Args:
        user_message (str): The message sent by the user.
        system_prompt (str): The assistant's behavior description.
        model (str): The OpenAI model to use.
        max_tokens (int): Maximum tokens in the response.

    Returns:
        dict: { success: bool, reply/error: str }
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=max_tokens
        )

        reply = response.choices[0].message.content
        return {
            "success": True,
            "reply": reply.strip()
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"OpenAI error: {str(e)}"
        }
