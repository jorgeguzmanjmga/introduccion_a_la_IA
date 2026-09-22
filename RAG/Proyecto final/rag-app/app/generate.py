import os
from typing import List, Dict, Any
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

raw_gen_model = os.getenv("GENERATION_MODEL", "models/gemini-3.6-flash")
GENERATION_MODEL = raw_gen_model if raw_gen_model.startswith("models/") else f"models/{raw_gen_model}"

MIN_RELEVANCE_SCORE = 0.60


def format_context(citations: List[Dict[str, Any]]) -> str:
    """Formatea los fragmentos recuperados para inyectarlos en el prompt."""
    blocks = []
    for item in citations:
        cid = item["citation_id"]
        source = item["source"]
        page = item["page"]
        text = item["text"]
        blocks.append(f"[{cid}] (Fuente: {source}, Diapositiva {page}):\n{text}")
    return "\n\n".join(blocks)


def generate_rag_response(question: str, citations: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Evalúa evidencia y solicita a Gemini una respuesta anclada con citas numéricas.
    Si se abstiene, vacía la lista de citas.
    """
    # 1. Filtro heurístico de abstención por score
    if not citations or citations[0].get("score", 0.0) < MIN_RELEVANCE_SCORE:
        return {
            "answer": "No dispongo de evidencia suficiente en el material de clase para responder a esta pregunta.",
            "citations": [],   # <-- Lista vacía: nada que mostrar
            "abstained": True
        }

    context_str = format_context(citations)

    system_instruction = (
        "Eres un asistente docente universitario riguroso. Tu objetivo es responder preguntas "
        "única y exclusivamente con base en la evidencia provista en los fragmentos.\n"
        "Reglas obligatorias:\n"
        "1. Responde en español de forma clara, técnica y concisa.\n"
        "2. Ancla cada afirmación usando citas numéricas entre corchetes, p. ej. [1], [2], correspondientes a los fragmentos.\n"
        "3. Si los fragmentos no contienen información directa para responder a la pregunta, di textualmente: "
        "'No dispongo de evidencia suficiente en el material de clase para responder a esta pregunta.'\n"
        "4. No utilices conocimiento externo ni asumas datos que no figuren en los textos provistos."
    )

    prompt = (
        f"Pregunta del alumno:\n{question}\n\n"
        f"Evidencia disponible:\n{context_str}\n\n"
        "Respuesta:"
    )

    try:
        response = client.models.generate_content(
            model=GENERATION_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.1
            )
        )

        raw_answer = response.text.strip() if response.text else "No dispongo de evidencia suficiente en el material de clase para responder a esta pregunta."
        abstained = "no dispongo de evidencia suficiente" in raw_answer.lower()

        # Si el modelo determinó abstenerse aunque el score estuviera al límite, no enviamos citas
        final_citations = [] if abstained else citations

        return {
            "answer": raw_answer,
            "citations": final_citations,
            "abstained": abstained
        }

    except Exception as e:
        return {
            "answer": f"Error al generar respuesta con Gemini: {str(e)}",
            "citations": [],
            "abstained": True
        }