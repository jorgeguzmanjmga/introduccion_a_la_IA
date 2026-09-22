# Tutor RAG - Material de Clase

Sistema RAG para consulta de diapositivas de clase (PDF) usando FastAPI, Streamlit, ChromaDB y Google Gemini.

---

## Requisitos Previos

- Python 3.10+
- Clave de API de [Google AI Studio](https://aistudio.google.com/apikey)

---

## Instalación

1. **Crear y activar entorno virtual:**
   ```bash
   python -m venv venv
   # En Windows:
   venv\Scripts\activate
   # En Linux/macOS:
   source venv/bin/activate
    ```
2. **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Configurar variables de entorno:**
    Crea un archivo .env a partir de .env.example con tu clave
    ```bash
    GOOGLE_API_KEY=tu_clave_de_google_ai_aqui
    EMBEDDING_MODEL=models/gemini-embedding-001
    GENERATION_MODEL=models/gemini-3.6-flash
    ```
## Ejecución

Abre dos terminales con el entorno virtual activado:

**Terminal 1 — Backend (FastAPI):**
```bash
uvicorn app.main:app --reload --port 8000
```
- Swagger UI / Documentación: `http://localhost:8000/docs`

**Terminal 2 — Frontend (Streamlit):**
```bash
streamlit run ui/streamlit_app.py
```
- Interfaz web: `http://localhost:8501`

---

## Flujo de Uso

1. Abre `http://localhost:8501`.
2. En la barra lateral, sube las presentaciones PDF de clase y presiona **"Indexar documentos"**.
3. Realiza preguntas sobre el contenido en la caja de texto central.
4. El sistema responde con citas numeradas `[n]` y muestra los fragmentos utilizados como evidencia. Si la pregunta no se responde con el material, el sistema se abstiene explícitamente.

---

## Estructura

```text
rag-app/
├── app/
│   ├── main.py          # API FastAPI
│   ├── chunk.py         # Extracción de PDF
│   ├── embed.py         # Generación de embeddings con Google AI
│   ├── store.py         # Persistencia vectorial en ChromaDB
│   └── generate.py      # Generación de respuesta con Gemini y citas
├── ui/
│   └── streamlit_app.py # Interfaz de usuario en Streamlit
├── data/                # PDFs del curso
├── requirements.txt
└── .env.example
```