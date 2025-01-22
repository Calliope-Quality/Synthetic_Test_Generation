# test_openai_call.py
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=openai_api_key)
GPT_MODEL = 'gpt-4o'  # Use a known model for testing

prompt = "Write a short poem about testing AI."

try:
    response = client.chat.completions.create(
        model=GPT_MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    print("Response choices length:", len(response.choices))
    print("First choice:", response.choices[0].message.content if response.choices else "No choices")
except Exception as e:
    print("Error during API call:", e)