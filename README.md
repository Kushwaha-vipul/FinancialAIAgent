#  FinancialAIAgent – AI-Powered Financial Assistant

FinAgentX is an AI-driven financial assistant that helps users with **financial queries, insights, and auto-generated reports (PDF & PPT)**.  
It combines **Natural Language Processing, Knowledge Retrieval, and Report Generation** to deliver  results. 

---

## Features

- **Smart Financial Q&A** – Ask any finance-related question (e.g., stock market trends, savings, retirement planning).  
-  **Knowledge Base Support** – Ingest and query from your own documents (PDF/TXT).  
-  **Auto-Generated Reports** – Get answers exported as professional **PDF and PPT reports**.  
-  **FastAPI Backend** – Efficient and production-ready REST API.  
-  **React Frontend (with TailwindCSS)** – Clean and responsive UI.  
-  **End-to-End Flow** – User Query → Embedding → Vector DB Search → LLM Synthesis → Report Generator → PDF/PPT Download

---

## Tech Stack

**Backend**  
- Python 3.10+  
- FastAPI  
- OpenAI API (LLM & embeddings)  
- ChromaDB (Vector database for document search)  
- ReportLab (PDF generation)  
- python-pptx (PowerPoint generation)  

**Frontend**  
- React + TypeScript  
- TailwindCSS  
- Vite (for fast development server)  

---

##  Project Structure


FinancialAIAgent/
│── agents/                      # AI agents (ingestion, retriever, synthesizer, etc.)
│── core/                        # LLM client & utilities
│── data/                        # Knowledge base documents (PDF/TXT)
│── db/                          # Local ChromaDB storage
│── frontend/                    # React + Tailwind frontend
│── utils/                       # Report generator & logging utils
│── main.py                      # FastAPI backend entrypoint
│── requirements.txt             # Python dependencies
│── package.json                 # Frontend dependencies
│── README.md                    # Project documentation




##  Setup & Installation

### Clone the repository

git clone https://github.com/Kushwaha-vipul/FinancialAIAgent.git
cd FinancialAIAgent

## Setup Python backend

python -m venv venv
source venv/bin/activate   
pip install -r requirements.txt


## Create a .env file in root:


OPENAI_API_KEY=your_openai_api_key_here

## Run document ingestion:


python -m agents.ingest

## Start backend:


uvicorn main:app --reload
Visit docs: http://127.0.0.1:8000/docs

## Setup React frontend

cd frontend
npm install
npm run dev



##  End-to-End Workflow

The complete pipeline of **FinancialAIAgent** works as follows:

1. **User Query (Frontend)**  
   - The user enters a query in the React-based UI .
   - Query is sent to the FastAPI backend.

2. **Knowledge Retrieval (Backend)**   
     - The system generates an **embedding vector** for the query using OpenAI’s embedding model.  
     - ChromaDB (vector database) is searched for semantically similar documents from the `data/` folder.  
     - Relevant passages are returned as supporting context.  

3. **AI Reasoning (LLM)**  
   - The query + retrieved context is passed to the selected LLM .  
   - The LLM synthesizes a final answer by combining user query + financial knowledge + retrieved documents.  

4. **Report Generation**  
   - The AI response is sent to the `report_generator`.  
   - Two formats are auto-created:  
     -  **PDF** (via ReportLab) – clean structured report with title + content.  
     -  **PPTX** (via python-pptx) – title slide + content slide(s).  

5. **Response Back to User**   
     - Generated answer (text).  
     - Downloadable links to `report.pdf` and `report.pptx`.   

6. **Frontend Display**  
   - User sees instant text response in the UI.  
   - Can click to **download PDF/PPT reports** for offline use.  

