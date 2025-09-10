
from core.llm_client import chat_with_llm
from typing import List
from utils.logging import logger

def synthesize_response(query: str, docs: List[str], model: str) -> str:
    """
    Combines user query + retrieved docs for AI response.
    """
    context = "\n".join(docs) if docs else "No external knowledge used."
    prompt = f"""
    You are a finance AI assistant.
    Answer the user's query using the following documents as context.

    Query: {query}
    Documents:
    {context}
    """
    response = chat_with_llm(prompt, model=model)
    logger.info(f"Synthesized AI response length: {len(response)}")
    return response
