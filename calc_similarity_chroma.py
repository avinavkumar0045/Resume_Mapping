import numpy as np
import chromadb.utils.embedding_functions as embedding_functions

# We can just use the default Chroma ONNX model which IS all-MiniLM-L6-v2
ef = embedding_functions.DefaultEmbeddingFunction()

question = "What are some of tourist place in varanashi?"
answers = [
    "Tourist place in varnashi is Sangam", # here embedding does not work , cause it only searches tokens 
    "Kashi viswanath",
    "Dashaswamegh ghat",
    "There is no tourist place in varanashi."
]

print("Computing embeddings...")
# Default function takes a list of documents
embeddings = ef([question] + answers)

q_emb = np.array(embeddings[0])
a_embs = np.array(embeddings[1:])

# Cosine similarity: dot product / (norm(q) * norm(a))
def cosine_sim(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

print("\n--- Cosine Similarity Results ---")
print(f"Question: '{question}'\n")

best_score = -1
best_ans = ""

for i, ans in enumerate(answers):
    sim = cosine_sim(q_emb, a_embs[i])
    print(f"Similarity: {sim:.4f} | Answer: '{ans}'")
    if sim > best_score:
        best_score = sim
        best_ans = ans
        
print(f"\n=> Best Match: '{best_ans}' (Score: {best_score:.4f})")
