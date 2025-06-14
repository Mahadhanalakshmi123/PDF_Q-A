from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from backend.loader import load_pdf_text, chunk_text
from backend.embed_store import EmbedStore
from backend.qa import answer_with_context

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

store = EmbedStore()

@app.post("/upload")
async def upload(pdf: UploadFile = File(...)):
    pdf_bytes = await pdf.read()
    text = load_pdf_text(pdf_bytes)
    chunks = chunk_text(text)
    store.build(chunks)
    return {"chunks": len(chunks)}

@app.get("/ask")
async def ask(q: str):
    try:
        contexts = store.query(q)
        answer = answer_with_context(q, contexts)
        return {"answer": answer}
    except Exception as e:
        return {"error": str(e)}"
