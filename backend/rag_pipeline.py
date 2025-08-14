import requests
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

# Config
QDRANT_HOST = "localhost"
QDRANT_PORT = 6333
OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3:8b"
COLLECTION_NAME = "documents"

# Init clients
qdrant = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
embedder = SentenceTransformer("all-MiniLM-L6-v2")

def search_docs(query: str, top_k: int = 5):
    """Search for relevant docs in Qdrant."""
    vector = embedder.encode(query).tolist()
    results = qdrant.search(
        collection_name=COLLECTION_NAME,
        query_vector=vector,
        limit=top_k
    )
    return [hit.payload.get("text", "") for hit in results]

def handle_rag_query(question: str) -> str:
    """Retrieve context from Qdrant and query LLaMA for an answer"""
    docs = search_docs(question)
    context = "\n\n".join(docs)

    prompt = f"""
    you are a knowledgable assistant.
    Use the following context to answer the question truthfully.
    If the answer is not in the context, say "I don't know".

    Context:
    {context}

    Question: {question}

    """ 

    response = requests.post(
        OLLAMA_API_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }
    )

    if response.status_code != 200:
        raise Exception(f"Ollama API error: {response.text}")
    
    data = response.json()
    return data.get("response", "").strip()

# Test the pipeline
if __name__ == "__main__":
    print(handle_rag_query("What is the capital of France?"))

