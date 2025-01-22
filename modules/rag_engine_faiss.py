# modules/rag_engine_faiss.py
import os
from logger import logger
from utils.vector_db_faiss import search_similar
from utils.embeddings import generate_embedding
from openai import OpenAI
from helper import get_openai_api_key

def generate_test_cases(processed_story):
    """
    Generate synthetic test cases for the given processed story using a
    Retrieval-Augmented Generation approach, incorporating similar past
    test cases retrieved from the FAISS index.
    """
    try:
        # Retrieve API key and initialize OpenAI client
        openai_api_key = get_openai_api_key()
        client = OpenAI(api_key=openai_api_key)

        # Define the model to be used (adjust if necessary)
        GPT_MODEL = 'gpt-4o'  # Change this if needed

        # Generate an embedding for the processed user story
        story_embedding = generate_embedding(processed_story)

        # Retrieve similar test cases from FAISS
        similar_contexts = search_similar(story_embedding, top_k=5)

        # Combine retrieved contexts into a single string for the prompt
        context_text = "\n".join(similar_contexts) if similar_contexts else ""

        # Construct the prompt using retrieved context and the processed story
        structured_prompt = f"""
You are an expert QA and compliance analyst. Review the following user story and generate **no more than 10** synthetic test cases. 
Ensure that the test cases:
- Follow QA best practices (including both positive and negative tests).
- Identify potential issues that CAST or other security audits might flag.
- Adhere to Behavioral Health compliance standards.
- Observe EMR (Electronic Medical Record) best practices.
- Incorporate compliance with user story Behavioral Health best practices.
- Incorporate specific patterns, scenarios, and details similar to those found in relevant past test cases retrieved from the vector database.

Relevant Past Test Cases:
{context_text}

For each test case, provide a concise description and expected outcome.

User Story:
{processed_story}

Generate Test Cases:
"""

        # Create the API request using the constructed prompt
        response = client.chat.completions.create(
            model=GPT_MODEL,
            messages=[{
                "role": "user",
                "content": structured_prompt
            }]
        )

        # Log the length of choices for debugging
        choices_length = len(response.choices) if hasattr(response, 'choices') else 'N/A'
        logger.debug(f"Response choices length: {choices_length}")

        # Attempt to extract the content safely
        try:
            generated_content = response.choices[0].message.content
        except (IndexError, AttributeError) as e:
            logger.error(f"Error accessing response content: {e}")
            logger.error(f"Full response: {response}")
            return None

        logger.debug(f"API response received: {generated_content}")
        return generated_content

    except Exception as e:
        logger.error(f"Error during test case generation: {e}")
        return None