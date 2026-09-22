import os
import shutil
from typing import List, Optional
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from app.chunk import process_pdf
from app.embed import get_embeddings_batch, get_embedding
from app.store import add_documents, query_similar, count_documents, reset_collection, get_sources_breakdown
from app.generate import generate_rag_response

load_dotenv()

app = FastAPI(
    title="RAG Educational Assistant API",
    version="1.0.0",
    description="API de ingestión y consulta RAG para material docente"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Esquemas de entrada y salida
class QueryRequest(BaseModel):
    question: str
    top_k: Optional[int] = 4

class Citation(BaseModel):
    citation_id: int
    text: str
    source: str
    page: int
    score: float

class QueryResponse(BaseModel):
    answer: str
    citations: List[Citation]
    abstained: bool

class IngestResponse(BaseModel):
    indexed_documents: int
    indexed_chunks: int
    total_stored_chunks: int



@app.get("/health", tags=["Status"])
def health():
    """Confirma que la API está viva y reporta el estado de ChromaDB."""
    return {
        "status": "healthy",
        "stored_chunks": count_documents(),
        "sources": get_sources_breakdown(),  # <-- Añadimos el desglose aquí
        "embedding_model": os.getenv("EMBEDDING_MODEL", "models/gemini-embedding-001"),
        "generation_model": os.getenv("GENERATION_MODEL", "models/gemini-3.6-flash")
    }


@app.post("/ingest", response_model=IngestResponse, tags=["Index"])
async def ingest_documents(files: List[UploadFile] = File(...)):
    """
    Recibe múltiples PDFs en memoria, extrae chunks, calcula embeddings en lotes
    y los indexa en ChromaDB sin tocar carpetas temporales en disco.
    """
    all_chunks = []
    processed_files_count = 0

    for file in files:
        if not file.filename.lower().endswith(".pdf"):
            continue

        # Leer directamente a memoria (elimina cualquier WinError 5 de Windows)
        file_bytes = await file.read()
        chunks = process_pdf(file_bytes, file_name=file.filename)
        all_chunks.extend(chunks)
        processed_files_count += 1

    if not all_chunks:
        raise HTTPException(
            status_code=400,
            detail="No se extrajeron fragmentos válidos de los archivos subidos."
        )

    # Vectorización por lotes con Google AI
    texts = [c["text"] for c in all_chunks]
    embeddings = get_embeddings_batch(texts, batch_size=20)

    # Persistencia en ChromaDB
    added_count = add_documents(all_chunks, embeddings)

    return IngestResponse(
        indexed_documents=processed_files_count,
        indexed_chunks=added_count,
        total_stored_chunks=count_documents()
    )


@app.post("/query", response_model=QueryResponse, tags=["RAG"])
def query_rag(request: QueryRequest):
    """
    Ejecuta el ciclo RAG: vectoriza la pregunta, recupera chunks top-k de ChromaDB
    y ancla la respuesta con Gemini.
    """
    cleaned_question = request.question.strip()
    if not cleaned_question:
        raise HTTPException(status_code=400, detail="La pregunta no puede estar vacía.")

    if count_documents() == 0:
        return QueryResponse(
            answer="El índice vectorial está vacío. Por favor ingesta documentos primero en /ingest.",
            citations=[],
            abstained=True
        )

    # 1. Embedding de la consulta
    q_vec = get_embedding(cleaned_question)

    # 2. Recuperación top-k en ChromaDB
    citations = query_similar(q_vec, top_k=request.top_k)

    # 3. Generación y regla de abstención con Gemini
    result = generate_rag_response(cleaned_question, citations)

    return QueryResponse(
        answer=result["answer"],
        citations=result["citations"],
        abstained=result["abstained"]
    )


@app.post("/reset", tags=["Admin"])
def reset_index():
    """Elimina la colección de ChromaDB para reindexar desde cero."""
    reset_collection()
    return {"message": "Índice vectorial vaciado correctamente.", "total_chunks": 0}