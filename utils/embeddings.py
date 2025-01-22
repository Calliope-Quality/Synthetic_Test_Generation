# utils/embedding.py
import os
from logger import logger
from dotenv import load_dotenv
from openai import OpenAI  # Import the new OpenAI class

load_dotenv()

def generate_embedding(text):
    """
    Generate an embedding for the given text using OpenAI's new embeddings API.
    Uses the small model "text-embedding-3-small".

    Args:
        text (str): The input text.

    Returns:
        list: The embedding vector.
    """
    try:
        client = OpenAI()
        response = client.embeddings.create(
            input=text,
            model="text-embedding-3-small"  # Using the small model
        )
        # Extract the embedding from the response
        embedding = response.data[0].embedding
        return embedding
    except Exception as e:
        logger.error(f"Error generating embedding: {e}")
        # Determine the dimension for the small model.
        # For illustration, we'll assume a dimension of 768.
        # Adjust this number based on the actual dimension of the small model.
        small_model_dimension = 1536
        return [0.0] * small_model_dimension