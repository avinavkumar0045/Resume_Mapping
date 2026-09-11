import numpy as np
import sys
try:
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "sentence-transformers", "scikit-learn"])
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity

# Initialize the model using the local directory we just downloaded
model = SentenceTransformer('./all-MiniLM-L6-v2')

question = "What are some of tourist place in varanashi?"
answers = [
    "Tourist place in varnashi is Sangam",
    "Tourist place in varnashi is Kashi viswanath",
    "Tourist place in varnashi is Dashaswamegh ghat",
    "There is no tourist place in varanashi."
]

# Get embeddings
q_emb = model.encode([question])
a_embs = model.encode(answers)

# Calculate cosine similarities
similarities = cosine_similarity(q_emb, a_embs)[0]

print("\n--- Cosine Similarity Results ---")
print(f"Question: '{question}'\n")
for ans, sim in zip(answers, similarities):
    print(f"Similarity: {sim:.4f} | Answer: '{ans}'")
    
# Find the best match
best_idx = np.argmax(similarities)
print(f"\n=> Best Match: '{answers[best_idx]}' (Score: {similarities[best_idx]:.4f})")
