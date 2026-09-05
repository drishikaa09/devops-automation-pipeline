"""
Takes an incoming error + retrieved runbooks, asks the LLM to reason
over them, and returns a structured decision. The LLM never executes
anything directly — it only returns JSON, which the Action Registry
then validates and (if approved) acts on.
"""
import os
import json
import pickle
import faiss
from sentence_transformers import SentenceTransformer
from google import genai

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
embed_model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.read_index("faiss_index.bin")
with open("faiss_metadata.pkl", "rb") as f:
    metadata = pickle.load(f)

SYSTEM_PROMPT = """You are the reasoning component of a DevOps incident remediation agent.
You never execute commands directly. You only return a structured JSON decision.

Given an error and retrieved runbook context, respond with ONLY valid JSON, no other text,
no markdown code fences:
{
  "decision": "AUTO_REMEDIATE" or "ESCALATE",
  "action": "<one of: RESTART_CONTAINER, RESOLVE_PORT_CONFLICT, RETRY_DEPENDENCY_INSTALL, ROLLBACK_DEPLOYMENT, RERUN_TEST_STAGE, or null if escalating>",
  "confidence": <float 0.0-1.0>,
  "reason": "<short explanation>",
  "runbook_id": "<id of the runbook that most informed this decision, or null>"
}

Only recommend AUTO_REMEDIATE if the runbook context clearly and unambiguously supports it.
When uncertain, escalate rather than guess."""


def retrieve_runbooks(error_text: str, k: int = 3):
    query_embedding = embed_model.encode([error_text], convert_to_numpy=True)
    distances, indices = index.search(query_embedding, k)
    return [metadata[idx] for idx in indices[0]]


def decide(error_text: str) -> dict:
    runbooks = retrieve_runbooks(error_text)
    context = "\n\n---\n\n".join(f"[runbook_id: {rb['runbook_id']}]\n{rb['text']}" for rb in runbooks)

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=f"Error:\n{error_text}\n\nRetrieved runbook context:\n{context}",
        config={"system_instruction": SYSTEM_PROMPT}
    )

    raw_text = response.text.strip()
    if raw_text.startswith("```"):
        raw_text = raw_text.strip("`").replace("json\n", "", 1)
    return json.loads(raw_text)


if __name__ == "__main__":
    test_error = "Container exited with code 137, docker logs show OOMKilled true"
    decision = decide(test_error)
    print(json.dumps(decision, indent=2))
