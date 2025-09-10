from dotenv import load_dotenv
import os
import PyPDF2
from openai import OpenAI
import chromadb
from utils.logging import logger


load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

DATA_DIR = "data"
chroma_client = chromadb.PersistentClient(path="db")
collection = chroma_client.get_or_create_collection("finance_docs")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))



def extract_text_from_pdf(filepath: str) -> str:
    """Extract text from a PDF file"""
    text = ""
    with open(filepath, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text

def ingest_documents():
    """Read all PDFs/txts from data/ and store embeddings into Chroma"""
    for fname in os.listdir(DATA_DIR):
        if not fname.endswith((".pdf", ".txt")):
            continue

        fpath = os.path.join(DATA_DIR, fname)
        logger.info(f"Ingesting {fpath}...")

        
        if fname.endswith(".pdf"):
            content = extract_text_from_pdf(fpath)
        else:
            with open(fpath, "r", encoding="utf-8") as f:
                content = f.read()

        if not content.strip():
            logger.warning(f"No content extracted from {fname}, skipping.")
            continue

        
        emb = client.embeddings.create(
            model="text-embedding-3-small",
            input=content
        )

       
        collection.add(
            documents=[content],
            embeddings=[emb.data[0].embedding],
            ids=[fname]
        )
        logger.info(f"Stored {fname} into vector DB.")

if __name__ == "__main__":
    ingest_documents()
    logger.info("All documents ingested successfully ")
