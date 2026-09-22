import os
from typing import List, Dict, Any
import chromadb
from dotenv import load_dotenv

load_dotenv()

# Ruta local donde Chroma guardará los archivos binarios y la base sqlite
CHROMA_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma")
COLLECTION_NAME = "course_materials"

# 1. Creamos el cliente que apunta a la carpeta local (no a la nube)
_client = chromadb.PersistentClient(path=CHROMA_DIR)


def get_collection():
    """
    Obtiene la colección existente o crea una nueva si no existe.
    Configuramos la métrica 'cosine' para medir distancias angulares entre vectores.
    """
    return _client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )


def add_documents(
    chunks: List[Dict[str, Any]],
    embeddings: List[List[float]]
) -> int:
    """
    Recibe la lista de chunks de app/chunk.py y los vectores de app/embed.py
    y los almacena en el índice local.
    """
    collection = get_collection()

    ids = []
    documents = []
    metadatas = []

    for i, chunk in enumerate(chunks):
        doc_source = chunk["metadata"]["source"]
        page = chunk["metadata"]["page"]
        
        # ID único por fragmento (ejemplo: clase_1_analisis_combinatorio.pdf_p3_5)
        chunk_id = f"{doc_source}_p{page}_{i}"

        ids.append(chunk_id)
        documents.append(chunk["text"])
        metadatas.append({
            "source": str(doc_source),
            "page": int(page)
        })

    # Guardamos en disco los 4 elementos: IDs, textos, vectores y metadatos
    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )
    return len(ids)


def query_similar(
    query_embedding: List[float],
    top_k: int = 4
) -> List[Dict[str, Any]]:
    """
    Busca los 'top_k' fragmentos más cercanos al vector de la pregunta.
    """
    collection = get_collection()
    
    # Chroma busca por k-Nearest Neighbors (k-NN)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )

    formatted_results = []
    if results and results["documents"] and results["documents"][0]:
        docs = results["documents"][0]
        metas = results["metadatas"][0]
        distances = results["distances"][0]

        for idx, (doc, meta, dist) in enumerate(zip(docs, metas, distances), start=1):
            # Para la distancia coseno: 0 = idénticos, 2 = opuestos.
            # Convertimos la distancia en similitud: 1.0 - distancia
            similarity = round(1.0 - float(dist), 4)
            formatted_results.append({
                "citation_id": idx,
                "text": doc,
                "source": meta.get("source", "desconocido"),
                "page": meta.get("page", 0),
                "score": similarity
            })

    return formatted_results


def count_documents() -> int:
    """Devuelve cuántos chunks hay guardados en la colección actualmente."""
    collection = get_collection()
    return collection.count()

def reset_collection():
    """Elimina y recrea la colección para evitar acumulación de duplicados."""
    try:
        _client.delete_collection(name=COLLECTION_NAME)
    except Exception:
        pass
    return get_collection()

def get_sources_breakdown() -> dict:
    """Devuelve un diccionario con el nombre del documento y su cantidad de chunks."""
    try:
        col = get_collection()
        # Recuperamos solo los metadatos de toda la colección
        data = col.get(include=["metadatas"])
        metadatas = data.get("metadatas", [])
        breakdown = {}
        for meta in metadatas:
            if not meta: 
                continue
            src = meta.get("source", "Desconocido")
            breakdown[src] = breakdown.get(src, 0) + 1
        return breakdown
    except Exception:
        return {}