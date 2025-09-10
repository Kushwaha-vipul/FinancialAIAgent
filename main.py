from fastapi import FastAPI, Query
from pydantic import BaseModel
from config import AVAILABLE_MODELS
from core.llm_client import chat_with_llm
from core.llm_client import client

from utils.report_generator import generate_ppt, generate_pdf
from agents.retriever import retrieve
from agents.synthesizer import synthesize_response
from utils.logging import logger  


from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(title="FinAgentX", version="0.2")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if not os.path.exists("reports"):
    os.makedirs("reports")


app.mount("/reports", StaticFiles(directory="reports"), name="reports")


@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Server is running!"}


class QueryRequest(BaseModel):
    query: str

@app.post("/generate")
def generate_report(
    req: QueryRequest,
    model: str = Query("gpt-5", enum=list(AVAILABLE_MODELS.keys())),
    use_knowledge: bool = Query(True)
):
   
    logger.info(f"Query received: {req.query} | Model: {model} | KB: {use_knowledge}")

    
    docs = retrieve(req.query) if use_knowledge else []
    logger.info(f"Retrieved documents count: {len(docs)}")

    
    ai_response = synthesize_response(req.query, docs, model=model)
    logger.info(f"AI response length: {len(ai_response)}")

  
    ppt_file = generate_ppt("Finance Report", ai_response, filename="report.pptx")
    pdf_file = generate_pdf("Finance Report", ai_response, filename="report.pdf")
    logger.info(f"PPT and PDF generated: {ppt_file}, {pdf_file}")


    return {
        "query": req.query,
        "result": ai_response,
        "ppt_file": f"reports/report.pptx",
        "pdf_file": f"reports/report.pdf",
        "retrieved_docs": docs
    }
