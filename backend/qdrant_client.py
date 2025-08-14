# Vector Search with Qdrant

from qdrant_client import QdrantClient 
from sentence_transformers import SentenceTransformer

qdrant = QdrantClient("localhost", port=6333)
embedder = SentenceTransformer('all-MiniLM-L6-v2')

def search_docs(query, top_k=5):
    vector = embedder.encode(query).tolist()
    results = qdrant.search(
        collection_name = "documents",
        query_vector=vector,
        limit=top_k
    )
    return [hit.payload for hit in results]