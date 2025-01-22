import re
import os
import numpy as np

import chromadb
import chromadb.utils.embedding_functions as embedding_functions
from dotenv import load_dotenv
from config import DEBUG  # Import the global DEBUG flag from your config

# Load environment variables (e.g., OPENAI_API_KEY)
load_dotenv()

if DEBUG:
    print("[rag_engine_chroma] Initializing PersistentClient for ChromaDB...")

# IMPORTANT: Use the absolute path to your 143MB Chroma DB
CHROMA_PATH = "path/chroma_db" #put in the local of your chromadb once created

# Create a Persistent Client that points to your existing DB
client = chromadb.PersistentClient(path=CHROMA_PATH)

if DEBUG:
    print("[rag_engine_chroma] Setting up OpenAIEmbeddingFunction and retrieving collection...")

openai_api_key = os.getenv("OPENAI_API_KEY")
embedding_func = embedding_functions.OpenAIEmbeddingFunction(
    api_key=openai_api_key,
    model_name="text-embedding-3-small"
)

collection = client.get_or_create_collection(
    name="testrail_test_cases",
    embedding_function=embedding_func,
    metadata={"description": "TestRail test cases stored with Chroma"}
)

# Optional set of stop words to remove from user story
STOP_WORDS = {
    "the", "it", "is", "to", "and", "a", "in", "of", "that", "this", "etc", "for", "on"
}

def remove_stop_words(text: str) -> str:
    tokens = re.split(r"\s+", text)
    filtered_tokens = [t for t in tokens if t.lower() not in STOP_WORDS]
    if DEBUG:
        print(f"[rag_engine_chroma] Removed stop words. Original length: {len(tokens)}, Filtered length: {len(filtered_tokens)}")
    return " ".join(filtered_tokens)


def search_similar_chroma(story_embedding, top_k=5):
    """
    Queries the Chroma collection with the provided embedding, returning
    the top_k most similar documents.
    """
    if DEBUG:
        print(f"[rag_engine_chroma] Querying Chroma for top {top_k} similar documents...")

    results = collection.query(
        query_embeddings=[story_embedding],
        n_results=top_k,
        include=["documents"]
    )

    # Check if any documents returned
    if not results or "documents" not in results or len(results["documents"]) == 0:
        if DEBUG:
            print("[rag_engine_chroma] No similar documents found.")
        return []

    # For a single query embedding, results["documents"][0] is the list of top_k docs
    similar_docs = results["documents"][0]

    if DEBUG and similar_docs:
        sample_preview = similar_docs[0][:200]
        print(f"[rag_engine_chroma] Found similar documents. First doc preview:\n{sample_preview}...")

    return similar_docs


def generate_test_cases_chroma(processed_story: str):
    """
    Takes a user story, cleans it, generates an embedding, queries Chroma for similar test cases,
    and then calls OpenAI to generate synthetic test cases. Returns a string containing the test
    cases or an error message.
    """
    try:
        if DEBUG:
            print("[rag_engine_chroma] Starting test case generation with Chroma RAG...")

        cleaned_story = remove_stop_words(processed_story)
        if DEBUG:
            print(f"[rag_engine_chroma] Cleaned user story (preview): {cleaned_story[:100]}...")

        # 1) Generate embedding
        if DEBUG:
            print("[rag_engine_chroma] Generating embedding for the user story...")
        embedding_result = embedding_func(cleaned_story)

        # --- Combine chunked embeddings if necessary ---
        if isinstance(embedding_result, list) and len(embedding_result) > 0:
            first_elem = embedding_result[0]
            # If we have multiple arrays in a list => average them
            if isinstance(first_elem, list) and len(first_elem) > 1:
                if DEBUG:
                    print(f"[rag_engine_chroma] Embedding function returned {len(first_elem)} chunks, averaging them...")
                chunk_arrays = np.array(first_elem)  # shape: (#chunks, embedding_dim)
                story_embedding = np.mean(chunk_arrays, axis=0).tolist()
            elif isinstance(first_elem, np.ndarray):
                # Single chunk => flatten to Python list
                story_embedding = first_elem.tolist()
            else:
                # Some other shape => fallback
                story_embedding = embedding_result
        else:
            # No list or empty => fallback
            story_embedding = embedding_result

        # 2) Query Chroma for similar test cases
        similar_contexts = search_similar_chroma(story_embedding, top_k=5)
        if not similar_contexts:
            if DEBUG:
                print("[rag_engine_chroma] No similar contexts returned from Chroma.")
            return "ERROR: No relevant test cases found in Chroma for the user story."

        context_text = "\n".join(similar_contexts)
        if DEBUG:
            print(f"[rag_engine_chroma] Context text from top {len(similar_contexts)} test cases (preview): {context_text[:200]}...")

        # 3) Construct prompt
        structured_prompt = f"""
You are an expert QA and compliance analyst. Review the following user story and generate **no more than 10** synthetic test cases. 
Ensure that the test cases:
- Follow QA best practices (including positive & negative tests).
- Identify potential issues (like security audits).
- Adhere to Behavioral Health compliance standards.
- Observe EMR best practices.
- Incorporate relevant patterns found in past test cases from the vector database.

Please number each test case and provide a 'Title', 'Description', and 'Steps'. Format them as:

Test Case 1
Title: ...
Description: ...
Steps:
1) ...
2) ...
Expected: ...
---

Test Case 2
Title: ...
Description: ...
Steps:
1) ...
2) ...
Expected: ...
---

And so on.

Relevant Past Test Cases:
{context_text}

User Story:
{processed_story}

Generate Test Cases:
"""
        if DEBUG:
            print("[rag_engine_chroma] Structured prompt created. Calling OpenAI API for completion...")

        # 4) Call OpenAI
        try:
            from openai import OpenAI
            client_openai = OpenAI(api_key=openai_api_key)
            GPT_MODEL = 'gpt-4o'  # or whichever model you prefer

            response = client_openai.chat.completions.create(
                model=GPT_MODEL,
                messages=[{"role": "user", "content": structured_prompt}]
            )
            generated_content = response.choices[0].message.content

            # **FIX**: If GPT returns a list for any reason, join it into a single string
            if isinstance(generated_content, list):
                if DEBUG:
                    print("[rag_engine_chroma] GPT returned a list. Joining into one string.")
                generated_content = "\n".join(str(x) for x in generated_content)

            if not generated_content or generated_content.strip() == "":
                if DEBUG:
                    print("[rag_engine_chroma] OpenAI returned an empty or invalid response.")
                return "ERROR: OpenAI returned an empty response for test case generation."

            if DEBUG:
                print("[rag_engine_chroma] Received a valid response from OpenAI.")
                print(f"[rag_engine_chroma] Generated Test Cases (preview): {generated_content[:300]}...")

            return generated_content

        except Exception as openai_err:
            if DEBUG:
                print(f"[rag_engine_chroma] OpenAI error: {openai_err}")
            return f"ERROR: Failed calling OpenAI API: {openai_err}"

    except Exception as e:
        if DEBUG:
            print(f"[rag_engine_chroma] Unexpected error in generate_test_cases_chroma: {e}")
        return f"ERROR: Unexpected failure: {e}"