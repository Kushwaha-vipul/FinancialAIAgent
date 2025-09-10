import os
from typing import List
import chromadb
from utils.logging import logger
from openai import OpenAI


DATA_DIR = "data"  
EMBEDDING_MODEL = "text-embedding-3-small"  


chroma_client = chromadb.PersistentClient(path="db")
collection_name = "finance_docs"
collection = chroma_client.get_or_create_collection(name=collection_name)


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def list_documents() -> List[str]:
    """Return list of document filenames in data/"""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)
        logger.info(f"Created missing data directory: {DATA_DIR}")
    return [f for f in os.listdir(DATA_DIR) if f.endswith((".txt", ".pdf"))]


def retrieve(query: str, top_k: int = 3) -> List[str]:
    """
    Retrieve relevant documents using vector similarity.
    Falls back to listing files if collection is empty.
    """
    if collection.count() == 0:
        docs = list_documents()[:top_k]
        logger.info(f"Vector DB empty, fallback docs: {docs}")
        return docs

    
    q_emb = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=query
    ).data[0].embedding

    
    results = collection.query(
        query_embeddings=[q_emb],
        n_results=top_k
    )

    retrieved_docs = []
    if "documents" in results:
        for res in results["documents"]:
            retrieved_docs.extend(res)

    logger.info(f"Retrieved {len(retrieved_docs)} docs from vector DB")
    return retrieved_docs
