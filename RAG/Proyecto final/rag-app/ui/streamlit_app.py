import streamlit as st
import httpx

API_BASE_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Tutor RAG - Material de Clase",
    page_icon="📚",
    layout="centered", # Centrado da un aspecto más formal a la lectura
    initial_sidebar_state="expanded"
)

# --- INYECCIÓN DE DISEÑO CSS (Estilo Anthropic / Claude) ---
st.markdown("""
<style>
    /* Tipografía y colores base */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: #2D2D2D;
    }
    
    /* Fondo principal y barra lateral */
    .stApp {
        background-color: #FAFAFA;
    }
    [data-testid="stSidebar"] {
        background-color: #F3F3F1;
        border-right: 1px solid #E5E5E5;
    }
    
    /* Títulos elegantes */
    h1 {
        font-weight: 600 !important;
        color: #1A1A1A !important;
        letter-spacing: -0.02em !important;
    }
    h2, h3 {
        font-weight: 500 !important;
        color: #333333 !important;
    }
    
    /* Estilizar los contenedores nativos con borde para que parezcan tarjetas limpias */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FFFFFF;
        border-radius: 8px;
        padding: 0.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.02);
        margin-bottom: 1rem;
    }
    
    /* Botones minimalistas */
    .stButton > button {
        border-radius: 6px;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    /* Ocultar elementos ruidosos de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {background: transparent !important;}
</style>
""", unsafe_allow_html=True)

# --- CABECERA ---
st.markdown("<h1>📚 Asistente de Estudio</h1>", unsafe_allow_html=True)
st.markdown("<p style='font-size: 1.1rem; color: #555; margin-bottom: 2rem;'>Consulta tus apuntes y diapositivas de clase. El sistema fundamentará sus respuestas citando los documentos.</p>", unsafe_allow_html=True)

# --- BARRA LATERAL ---
with st.sidebar:
    st.markdown("### ⚙️ Configuración del Índice")
    
    try:
        health_resp = httpx.get(f"{API_BASE_URL}/health", timeout=3.0)
        if health_resp.status_code == 200:
            info = health_resp.json()
            total_chunks = info.get("stored_chunks", 0)
            sources = info.get("sources", {})
            
            st.success("🟢 App Conectada")
            
            # Desglose de documentos elegante
            st.markdown(f"**Total indexado:** {total_chunks} fragmentos")
            if sources:
                st.markdown("<hr style='margin: 0.5rem 0; opacity: 0.2;'>", unsafe_allow_html=True)
                for doc, count in sources.items():
                    # Muestra un ícono de documento, el nombre y los chunks sutilmente
                    st.markdown(f"<div style='font-size: 0.85rem; color: #555; padding: 2px 0;'>📄 <b>{doc}</b>: {count} chunks</div>", unsafe_allow_html=True)
                st.markdown("<hr style='margin: 0.5rem 0; opacity: 0.2;'>", unsafe_allow_html=True)
                
        else:
            st.error("⚠️ API con error")
    except Exception:
        st.error("❌ API no disponible")
        st.stop()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📥 Actualizar Material")
    uploaded_files = st.file_uploader(
        "Subir nuevas diapositivas (PDF)",
        type=["pdf"],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )

    if st.button("Indexar documentos", type="primary", use_container_width=True):
        if not uploaded_files:
            st.warning("Selecciona al menos un archivo PDF.")
        else:
            with st.spinner("Procesando material..."):
                files_payload = [("files", (f.name, f.getvalue(), "application/pdf")) for f in uploaded_files]
                try:
                    with httpx.Client(timeout=httpx.Timeout(300.0, connect=15.0)) as client_http:
                        resp = client_http.post(f"{API_BASE_URL}/ingest", files=files_payload)
                    if resp.status_code == 200:
                        st.success("¡Documentos indexados correctamente!")
                        st.rerun()
                    else:
                        st.error(f"Error en ingestión: {resp.text}")
                except Exception as e:
                    st.error(f"Error de conexión: {str(e)}")

    if st.button("Vaciar Índice (Reset)", use_container_width=True):
        try:
            httpx.post(f"{API_BASE_URL}/reset", timeout=5.0)
            st.info("Índice vaciado.")
            st.rerun()
        except Exception as e:
            st.error(str(e))


# --- ÁREA PRINCIPAL: CONSULTA ---
top_k = st.slider("Profundidad de búsqueda (fragmentos)", min_value=2, max_value=6, value=3)

question = st.text_input(
    "Tu pregunta:",
    placeholder="Ej: ¿Qué es una permutación y cómo se calcula?",
    label_visibility="collapsed"
)

col_ask, _ = st.columns([1, 4])
with col_ask:
    ask_pressed = st.button("Consultar", type="primary")

if ask_pressed:
    if not question.strip():
        st.warning("Por favor ingresa una pregunta.")
    else:
        with st.spinner("Analizando documentos y redactando respuesta..."):
            try:
                payload = {"question": question, "top_k": top_k}
                with httpx.Client(timeout=httpx.Timeout(60.0, connect=10.0)) as client_http:
                    res = client_http.post(f"{API_BASE_URL}/query", json=payload)

                if res.status_code == 200:
                    data = res.json()
                    answer = data["answer"]
                    citations = data.get("citations", [])
                    abstained = data.get("abstained", False)

                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    if abstained:
                        st.warning(answer)
                    else:
                        # Usamos un contenedor nativo con borde para preservar el renderizado Markdown/LaTeX
                        with st.container(border=True):
                            st.markdown(answer)

                    # Acordeones de evidencia elegantes
                    if not abstained and citations:
                        st.markdown("<p style='font-size: 0.9rem; color: #666; margin-top: 1rem; font-weight: 500;'>Fuentes referenciadas:</p>", unsafe_allow_html=True)
                        for c in citations:
                            with st.expander(f"[{c['citation_id']}] {c['source']} — Diapositiva {c['page']}"):
                                st.markdown(f"<div style='font-size: 0.9rem; color: #444; line-height: 1.5;'>{c['text']}</div>", unsafe_allow_html=True)
                                st.caption(f"Score de similitud: {c['score']:.4f}")
                else:
                    st.error(f"Error {res.status_code}: {res.text}")

            except Exception as e:
                st.error(f"No fue posible comunicarse con la API: {str(e)}")