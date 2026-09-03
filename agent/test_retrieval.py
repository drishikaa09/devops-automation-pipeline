import pickle
import faiss
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.read_index("faiss_index.bin")
with open("faiss_metadata.pkl", "rb") as f:
    metadata = pickle.load(f)

test_error = "Container exited with code 137, docker logs show OOMKilled true"
print(f"Query: {test_error}\n")

query_embedding = model.encode([test_error], convert_to_numpy=True)
distances, indices = index.search(query_embedding, k=3)

print("Top 3 matches:")
for rank, (idx, dist) in enumerate(zip(indices[0], distances[0]), 1):
    print(f"{rank}. {metadata[idx]['runbook_id']} (distance: {dist:.4f})")
