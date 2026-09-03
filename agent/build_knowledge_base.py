"""
Reads all runbook .txt files, embeds each one using sentence-transformers,
and builds a FAISS index for similarity search. Run this once to build
the index, and again any time a new verified-successful resolution is
added as a runbook.
"""
import os
import pickle
import faiss
from sentence_transformers import SentenceTransformer

RUNBOOKS_DIR = "runbooks"
INDEX_PATH = "faiss_index.bin"
METADATA_PATH = "faiss_metadata.pkl"

print("Loading embedding model (all-MiniLM-L6-v2)...")
model = SentenceTransformer("all-MiniLM-L6-v2")

runbook_files = sorted(f for f in os.listdir(RUNBOOKS_DIR) if f.endswith(".txt"))
print(f"Found {len(runbook_files)} runbooks: {runbook_files}")

texts = []
metadata = []

for filename in runbook_files:
    path = os.path.join(RUNBOOKS_DIR, filename)
    with open(path, "r") as f:
        content = f.read()
    texts.append(content)
    metadata.append({
        "runbook_id": filename.replace(".txt", ""),
        "filename": filename,
        "text": content,
    })

print("Embedding runbooks...")
embeddings = model.encode(texts, convert_to_numpy=True, show_progress_bar=True)

dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

faiss.write_index(index, INDEX_PATH)
with open(METADATA_PATH, "wb") as f:
    pickle.dump(metadata, f)

print(f"Done. Index has {index.ntotal} vectors of dimension {dimension}.")
print(f"Saved to {INDEX_PATH} and {METADATA_PATH}")
