from __future__ import annotations

import os
import sys
from pathlib import Path
import base64

import streamlit as st
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from rag.embed import embedder, reranker
from streamlit_app.rag_pipeline import answer_query, initialize_rag
from streamlit_app.ui_helpers import (
    apply_app_theme,
    ensure_upload_dir,
    persist_uploaded_pdf,
    render_chunks,
    render_header,
)

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_PDF = BASE_DIR / "data" / "deep-learning.pdf"


# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="RAG PDF QA",
    page_icon="📘",
    layout="wide",
)

apply_app_theme()
render_header()


# ===============================
# CACHE
# ===============================
@st.cache_data(show_spinner=False)
def cached_initialize_rag(pdf_path: str):
    return initialize_rag(pdf_path)


@st.cache_resource(show_spinner=False)
def cached_models():
    return embedder, reranker


# ===============================
# PDF VIEWER
# ===============================
@st.cache_data(show_spinner=False)
def cached_pdf_base64(pdf_path: str) -> str:
    with open(pdf_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def render_pdf(pdf_path: str):
    loader = st.empty()
    with loader.container():
        with st.spinner("Loading document preview..."):
            base64_pdf = cached_pdf_base64(pdf_path)

    pdf_display = f"""
        <iframe 
            src="data:application/pdf;base64,{base64_pdf}" 
            width="100%" 
            height="650px"
            style="border-radius:10px;"
        ></iframe>
    """
    loader.empty()
    st.markdown(pdf_display, unsafe_allow_html=True)


# ===============================
# RESOLVE PDF
# ===============================
def resolve_pdf_path(use_default_pdf: bool, uploaded_file) -> str | None:
    if use_default_pdf:
        if not DEFAULT_PDF.exists():
            raise FileNotFoundError(f"Default PDF not found at {DEFAULT_PDF}")
        return str(DEFAULT_PDF)

    if uploaded_file is None:
        return None

    upload_dir = ensure_upload_dir(str(BASE_DIR))
    content = uploaded_file.getvalue()
    return persist_uploaded_pdf(upload_dir, uploaded_file.name, content)


# ===============================
# PDF INPUT
# ===============================
st.subheader("Select Document")

col1, col2 = st.columns([3, 1])

with col1:
    uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

with col2:
    source_mode = st.segmented_control(
        "Document source",
        options=["Upload PDF", "Use default PDF"],
        default="Upload PDF",
        help="Choose whether to use your uploaded file or the default project PDF.",
    )
    use_default_pdf = source_mode == "Use default PDF"

if use_default_pdf and uploaded_file is not None:
    st.info("Default PDF is active. Uploaded file is ignored.")


# ===============================
# LOAD MODELS
# ===============================
cached_models()

# ===============================
# RESOLVE PDF
# ===============================
active_pdf = None

try:
    active_pdf = resolve_pdf_path(use_default_pdf, uploaded_file)
except Exception as exc:
    st.error(str(exc))


# ===============================
# SESSION STATE (IMPORTANT)
# ===============================
if "rag_data" not in st.session_state:
    st.session_state.rag_data = None

if "current_pdf" not in st.session_state:
    st.session_state.current_pdf = None


# ===============================
# PROCESS ONLY IF PDF CHANGES
# ===============================
if active_pdf and active_pdf != st.session_state.current_pdf:

    with st.spinner("Processing document..."):
        docs, index = cached_initialize_rag(active_pdf)

    st.session_state.rag_data = (docs, index)
    st.session_state.current_pdf = active_pdf


# ===============================
# MAIN UI
# ===============================
if not active_pdf:
    st.warning("Please upload or select a PDF.")
    st.stop()

docs, index = st.session_state.rag_data

st.success(f"Using: {os.path.basename(active_pdf)}")

left, right = st.columns([1.2, 1])

# ===============================
# LEFT → PDF VIEW
# ===============================
with left:
    st.markdown("###  Document Preview")
    render_pdf(active_pdf)


# ===============================
# RIGHT → QA
# ===============================
with right:

    st.markdown("### Ask Questions")

    with st.form("question_form"):
        query = st.text_input("Ask a question")
        submitted = st.form_submit_button("Get Answer")

    if submitted:

        if not query.strip():
            st.error("Please enter a valid question.")

        elif not os.getenv("GROQ_API_KEY"):
            st.error("Missing GROQ_API_KEY. Add it to your .env file.")

        else:
            with st.spinner("Thinking..."):
                answer, retrieved_chunks = answer_query(query, docs, index)

            st.markdown("### Answer")
            st.write(answer)

            with st.expander("Retrieved Context"):
                render_chunks(retrieved_chunks)