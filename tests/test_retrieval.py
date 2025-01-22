# test_retrieval.py
from utils.vector_db_faiss import initialize_faiss_index, search_similar
from utils.embeddings import generate_embedding

# Initialize or load FAISS index
initialize_faiss_index(dimension=1536)

# Use a sample text to generate an embedding
sample_query = "Example user scenario for testing retrieval."
embedding = generate_embedding(sample_query)

# Search the FAISS index
results = search_similar(embedding, top_k=5)
print("Retrieved similar items:", results)