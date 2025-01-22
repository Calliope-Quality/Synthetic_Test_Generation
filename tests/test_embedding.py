# test_embedding.py
from utils.embeddings import generate_embedding

sample_text = "Test embedding for diagnosis."
embedding = generate_embedding(sample_text)
print(f"Embedding length: {len(embedding)}")
print(f"First 5 elements: {embedding[:5]}")