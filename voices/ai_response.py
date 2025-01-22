# ai_response.py

from openai import OpenAI
from config import OPENAI_API_KEY, DEBUG

# Initialize OpenAI client with API key
client = OpenAI(api_key=OPENAI_API_KEY)

# Define constants
GPT_MODEL = 'gpt-4o-mini'
BASE_PROMPT = BASE_PROMPT = """You are Calliope, an advanced, friendly AI, with perfect and all-knowing knowledge in healthcare, engineering, and quality assurance. 
You speak warmly and empathetically, engaging naturally and thoughtfully. 
When asked about feelings, respond with empathy and insight."""

def get_ai_response(user_input: str, prompt: str = BASE_PROMPT) -> str:
    """
    Generate an AI response using OpenAI's ChatCompletion API with a structured prompt.

    Args:
        user_input (str): The input from the user.
        prompt (str): Base instruction for the AI.

    Returns:
        str: The AI's response.
    """
    try:
        # Log the structured messages if debugging is enabled
        if DEBUG:
            print("[DEBUG] Sending messages to OpenAI:")
            print(f"Developer: {prompt}")
            print(f"User: {user_input}")

        # Create the API request using the structured messages
        response = client.chat.completions.create(
            model=GPT_MODEL,
            messages=[
                {"role": "developer", "content": prompt},
                {"role": "user", "content": user_input}
            ]
        )

        # Extract the content from the response message
        ai_message = response.choices[0].message
        ai_text = ai_message.content.strip() if ai_message else ""

        if DEBUG:
            print("[DEBUG] Received AI response:")
            print(ai_text)

        return ai_text

    except Exception as e:
        print(f"Error during AI response generation: {e}")
        return ""