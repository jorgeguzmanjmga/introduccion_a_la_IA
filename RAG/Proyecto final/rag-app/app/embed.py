import os
import time
from typing import List
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai import errors

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("No se encontró GOOGLE_API_KEY en el entorno.")

client = genai.Client(api_key=api_key)

raw_model = os.getenv("EMBEDDING_MODEL", "models/gemini-embedding-001")
EMBEDDING_MODEL = raw_model if raw_model.startswith("models/") else f"models/{raw_model}"


def get_embedding(text: str) -> List[float]:
    """Genera el embedding de una sola consulta (query) con reintento si hay rate limit."""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = client.models.embed_content(
                model=EMBEDDING_MODEL,
                contents=text,
                config=types.EmbedContentConfig(
                    task_type="RETRIEVAL_QUERY"
                )
            )
            return response.embeddings[0].values
        except errors.ClientError as e:
            if "429" in str(e) and attempt < max_retries - 1:
                time.sleep(8.0)
                continue
            raise e


def get_embeddings_batch(texts: List[str], batch_size: int = 30) -> List[List[float]]:
    """
    Genera embeddings en lotes con pausas controladas y reintentos automáticos
    para respetar los límites de cuota (100 RPM).
    """
    all_embeddings: List[List[float]] = []

    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        max_retries = 5
        delay = 8.0

        for attempt in range(max_retries):
            try:
                response = client.models.embed_content(
                    model=EMBEDDING_MODEL,
                    contents=batch,
                    config=types.EmbedContentConfig(
                        task_type="RETRIEVAL_DOCUMENT"
                    )
                )
                for emb in response.embeddings:
                    all_embeddings.append(emb.values)
                break  # Éxito en este lote
            except errors.ClientError as e:
                if "429" in str(e) and attempt < max_retries - 1:
                    print(f"[Embedding 429] Límite de tasa alcanzado. Esperando {delay}s antes de reintentar...")
                    time.sleep(delay)
                    delay *= 1.5
                else:
                    raise e

        # Pausa preventiva entre lotes para no saturar la ventana de tiempo
        time.sleep(1.0)

    return all_embeddings