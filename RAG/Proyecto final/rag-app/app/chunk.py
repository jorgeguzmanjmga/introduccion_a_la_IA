import io
import re
from typing import List, Dict, Any, Union
from pypdf import PdfReader


def clean_text(text: str) -> str:
    """Limpia saltos de línea y normaliza artefactos de Beamer/LaTeX."""
    replacements = {
        "´ a": "á", "´ e": "é", "´ ı": "í", "´ i": "í", "´ o": "ó", "´ u": "ú",
        "´ A": "Á", "´ E": "É", "´ I": "Í", "´ O": "Ó", "´ U": "Ú", "˜ n": "ñ", "˜ N": "Ñ"
    }
    for old, new in replacements.items():
        text = text.replace(old, new)

    text = re.sub(r"\d+\s*/\s*\d+", "", text)
    text = re.sub(r"\n+", "\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def is_beamer_pause(curr_text: str, next_text: str) -> bool:
    """Determina si curr_text es un estado parcial de next_text por un \\pause."""
    curr_words = set(curr_text.split())
    next_words = set(next_text.split())

    if not curr_words:
        return True

    shared_ratio = len(curr_words.intersection(next_words)) / len(curr_words)
    return shared_ratio >= 0.85 and len(next_text) >= len(curr_text)


def split_text_into_chunks(
    text: str,
    chunk_size_words: int = 250,
    overlap_words: int = 50
) -> List[str]:
    """Divide textos extensos en bloques con solape."""
    words = text.split()
    if not words:
        return []

    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size_words
        chunks.append(" ".join(words[start:end]))
        if end >= len(words):
            break
        start += chunk_size_words - overlap_words

    return chunks


def process_pdf(
    source_input: Union[str, bytes, io.BytesIO],
    file_name: str = "documento.pdf",
    chunk_size_words: int = 250,
    overlap_words: int = 50
) -> List[Dict[str, Any]]:
    """
    Procesa un PDF (ruta local o stream en memoria) filtrando \\pause.
    """
    if isinstance(source_input, str):
        file_name = source_input.replace("\\", "/").split("/")[-1]
        reader = PdfReader(source_input)
    elif isinstance(source_input, bytes):
        reader = PdfReader(io.BytesIO(source_input))
    else:
        reader = PdfReader(source_input)

    raw_pages = []
    for page_idx, page in enumerate(reader.pages, start=1):
        cleaned = clean_text(page.extract_text() or "")
        if len(cleaned.split()) >= 8:
            raw_pages.append({"page": page_idx, "text": cleaned})

    final_pages = []
    total = len(raw_pages)

    for i in range(total):
        current_page = raw_pages[i]
        if i < total - 1:
            next_page = raw_pages[i + 1]
            if is_beamer_pause(current_page["text"], next_page["text"]):
                continue

        final_pages.append(current_page)

    all_chunks: List[Dict[str, Any]] = []
    for item in final_pages:
        words = item["text"].split()
        if len(words) <= chunk_size_words:
            all_chunks.append({
                "text": item["text"],
                "metadata": {"source": file_name, "page": item["page"]}
            })
        else:
            sub_chunks = split_text_into_chunks(item["text"], chunk_size_words, overlap_words)
            for sub in sub_chunks:
                all_chunks.append({
                    "text": sub,
                    "metadata": {"source": file_name, "page": item["page"]}
                })

    return all_chunks