# diagnose_rag_chroma.py

import os
import numpy as np
from dotenv import load_dotenv
import chromadb
import chromadb.utils.embedding_functions as embedding_functions

# Load environment variables
load_dotenv()

# ------------------------------
# 1) Initialize PersistentClient
# ------------------------------
# Use the exact absolute path to your 143MB Chroma DB
CHROMA_PATH = "/utils/chroma_db"
client = chromadb.PersistentClient(path=CHROMA_PATH)

# ------------------------------
# 2) Set up Embedding Function
# ------------------------------
openai_api_key = os.getenv("OPENAI_API_KEY")
embedding_func = embedding_functions.OpenAIEmbeddingFunction(
    api_key=openai_api_key,
    model_name="text-embedding-3-small"
)

# ------------------------------
# 3) Retrieve or Create Collection
# ------------------------------
# Make sure this matches the name used by your ingestion code
collection = client.get_or_create_collection(
    name="testrail_test_cases",  # must match ingestion
    embedding_function=embedding_func,
    metadata={"description": "TestRail test cases stored with Chroma"}
)

# ------------------------------
# 4) Minimal Ingestion Test
# ------------------------------
print("Performing minimal ingestion test...")

# Attempt to add a small document
doc_text = "Hello from the big 143MB DB!"
doc_id = "doc_hello_1"

collection.add(
    documents=[doc_text],
    ids=[doc_id]
)

# Verify it was inserted
verify_docs = collection.get(include=["documents", "metadatas"])
print("Minimal ingestion test retrieval:\n", verify_docs)

# ------------------------------
# 5) General Diagnostics
# ------------------------------

# A) Retrieve all documents (sample) to confirm data presence
print("\nAll documents in collection (sample):")
docs = collection.get(include=["documents", "metadatas"])
sample_docs = {k: v[:5] for k, v in docs.items() if isinstance(v, list)}
print(sample_docs)

# B) Test Embedding + Query
test_story = (
    "As a doctor, I want to check that my prescriptions can have a start date, "
    "so that my prescriptions are filled properly."
)
print("\nGenerating embedding for test story...")
cleaned_story = test_story  # or do additional filtering if you want
embedding_result = embedding_func(cleaned_story)

# Handle potential multiple chunks by averaging them
if isinstance(embedding_result, list) and len(embedding_result) > 0:
    first_elem = embedding_result[0]
    if isinstance(first_elem, list) and len(first_elem) > 1:
        print(f"Embedding function returned {len(first_elem)} chunks, averaging them...")
        chunk_arrays = np.array(first_elem)
        embedding = np.mean(chunk_arrays, axis=0).tolist()
    elif isinstance(first_elem, np.ndarray):
        print("Single chunk embedding obtained.")
        embedding = first_elem.tolist()
    else:
        embedding = embedding_result
else:
    embedding = embedding_result

print("Final embedding vector sample (first 5 dims):", embedding[:5] if isinstance(embedding, list) else embedding)

# Query with top_k=10
print("\nPerforming manual query with top_k=10...")
results = collection.query(
    query_embeddings=[embedding],
    n_results=10,
    include=["documents", "metadatas", "distances"]
)
print("Query results:")
print(results)

# Query with top_k=20
print("\nPerforming manual query with top_k=20...")
results_more = collection.query(
    query_embeddings=[embedding],
    n_results=20,
    include=["documents", "metadatas", "distances"]
)
print("Query results for top_k=20:")
print(results_more)