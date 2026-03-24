from __future__ import annotations

import hashlib
from pathlib import Path

import streamlit as st


def render_header() -> None:
    st.title("RAG-based PDF Question Answering")
    st.caption("Upload a PDF and ask questions grounded in its content.")


def apply_app_theme():
    st.markdown("""
    <style>
    .stApp {
        background: #f4f7ff;
        color: #0f172a;
    }

    .block-container {
        max-width: 1200px;
        padding-top: 1.5rem;
    }

    h1 {
        color: #1e3a8a;
        font-weight: 700;
    }

    /* Cards */
    section.main > div {
        background: white;
        border-radius: 12px;
        padding: 1rem;
    }

    /* Input */
    input {
        border-radius: 8px !important;
    }

    /* Button */
    button {
        background: #2563eb !important;
        color: white !important;
        border-radius: 8px !important;
    }

    /* Expander */
    .stExpander {
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown(
        """
        <style>
        /* ===== Base ===== */
        .stApp {
            background: #f6f9ff;
            color: #111827 !important;
        }

        .main .block-container {
            max-width: 1000px;
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        /* ===== Headings ===== */
        h1, h2, h3 {
            color: #0f172a !important;
        }

        p, span, label, div {
            color: #1f2937 !important;
        }

        /* ===== Cards ===== */
        [data-testid="stHorizontalBlock"] > div,
        [data-testid="stForm"],
        [data-testid="stExpander"],
        [data-testid="stStatusWidget"] {
            background: #f8fafc;
            border: 1px solid #e5e7eb;
            border-radius: 12px;
            padding: 1rem;
        }

        /* ===== File uploader ===== */
        [data-testid="stFileUploaderDropzone"] {
            border: 2px dashed #3b82f6 !important;
            background: #f0f6ff;
        }

        /* ===== Input ===== */
        .stTextInput input {
            color: #111827 !important;
            background: #ffffff !important;
            border: 1px solid #cbd5e1;
        }

        /* ===== Button ===== */
        .stButton button {
            background: #2563eb;
            color: white;
            border-radius: 8px;
            font-weight: 600;
        }

        .stButton button:hover {
            background: #1d4ed8;
        }

        /* ===== Alerts ===== */
        [data-testid="stAlert"] {
            color: #111827 !important;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <style>
        /* ===== Base Layout ===== */
        .stApp {
            background: linear-gradient(180deg, #f8fbff 0%, #eef4ff 100%);
            color: #0f172a;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }

        .main .block-container {
            max-width: 1000px;
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        /* ===== Headings ===== */
        h1 {
            color: #0b1f3a;
            font-weight: 700;
            letter-spacing: -0.3px;
        }

        h2, h3 {
            color: #1e3a8a;
            font-weight: 600;
        }

        /* ===== Cards / Sections ===== */
        [data-testid="stHorizontalBlock"] > div,
        [data-testid="stForm"],
        [data-testid="stExpander"],
        [data-testid="stStatusWidget"] {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 14px;
            padding: 1rem;
            box-shadow: 0 8px 24px rgba(15, 23, 42, 0.04);
        }

        /* ===== File Upload ===== */
        [data-testid="stFileUploaderDropzone"] {
            border: 2px dashed #3b82f6 !important;
            background: #f1f6ff;
            border-radius: 12px;
            transition: all 0.2s ease;
        }

        [data-testid="stFileUploaderDropzone"]:hover {
            background: #e6f0ff;
            border-color: #2563eb !important;
        }

        /* ===== Inputs ===== */
        .stTextInput > div > div > input {
            border: 1.5px solid #cbd5e1;
            border-radius: 10px;
            padding: 0.5rem;
            transition: all 0.2s ease;
        }

        .stTextInput > div > div > input:focus {
            border-color: #2563eb;
            box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.15);
        }

        /* ===== Buttons ===== */
        .stButton > button,
        div[data-testid="stFormSubmitButton"] > button {
            background: linear-gradient(90deg, #2563eb 0%, #3b82f6 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-weight: 600;
            padding: 0.5rem 1.2rem;
            transition: all 0.2s ease;
        }

        .stButton > button:hover,
        div[data-testid="stFormSubmitButton"] > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 10px 20px rgba(37, 99, 235, 0.25);
        }

        /* ===== Alerts ===== */
        [data-testid="stAlert"] {
            border-radius: 10px;
            border: 1px solid #dbeafe;
            background: #f0f7ff;
        }

        /* ===== Divider Line ===== */
        hr {
            border: none;
            height: 1px;
            background: #e2e8f0;
            margin: 1.5rem 0;
        }

        /* ===== Scrollbar (optional polish) ===== */
        ::-webkit-scrollbar {
            width: 8px;
        }

        ::-webkit-scrollbar-thumb {
            background: #c7d2fe;
            border-radius: 10px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: #93c5fd;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(180deg, #f5f9ff 0%, #edf4ff 50%, #e8f0ff 100%);
            color: #0f172a;
        }

        .main .block-container {
            max-width: 980px;
            padding-top: 1.5rem;
            padding-bottom: 2rem;
        }

        h1, h2, h3 {
            color: #0b2a52;
            letter-spacing: 0.1px;
        }

        [data-testid="stHorizontalBlock"] > div {
            background: #ffffff;
            border: 1px solid #d7e5ff;
            border-radius: 12px;
            padding: 0.55rem 0.7rem;
        }

        [data-testid="stForm"] {
            border: 1px solid #cfe0ff;
            border-radius: 12px;
            padding: 1rem;
            background: #ffffff;
            box-shadow: 0 6px 18px rgba(16, 36, 94, 0.06);
        }

        [data-testid="stFileUploaderDropzone"] {
            border: 1.5px dashed #8fb4ff !important;
            background: #f8fbff;
        }

        [data-testid="stFileUploaderDropzone"]:hover {
            border-color: #4f8dff !important;
            background: #eef5ff;
        }

        [data-testid="stSegmentedControl"] {
            background: #f8fbff;
            border: 1px solid #cfe0ff;
            border-radius: 12px;
            padding: 0.3rem;
        }

        [data-testid="stSegmentedControl"] button {
            border-radius: 9px !important;
            border: none !important;
            color: #1e3a8a !important;
            font-weight: 600 !important;
        }

        [data-testid="stSegmentedControl"] button[aria-pressed="true"] {
            background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%) !important;
            color: #1e3a8a !important;
            border: 1px solid #dbe7ff !important;
            box-shadow: 0 3px 10px rgba(15, 23, 42, 0.08);
        }

        .stTextInput > div > div > input {
            border: 1px solid #b9d1ff;
            background: #ffffff;
            color: #0f172a;
        }

        .stTextInput > div > div > input:focus {
            border-color: #3b82f6;
            box-shadow: 0 0 0 1px #3b82f6;
        }

        .stButton > button, div[data-testid="stFormSubmitButton"] > button {
            background: linear-gradient(90deg, #2563eb 0%, #3b82f6 100%);
            color: #ffffff;
            border: none;
            border-radius: 10px;
            font-weight: 600;
            transition: transform 0.08s ease, box-shadow 0.16s ease;
        }

        .stButton > button:hover, div[data-testid="stFormSubmitButton"] > button:hover {
            box-shadow: 0 6px 18px rgba(37, 99, 235, 0.28);
            transform: translateY(-1px);
        }

        [data-testid="stAlert"] {
            border-radius: 10px;
            border: 1px solid #d5e4ff;
        }

        [data-testid="stStatusWidget"] {
            border: 1px solid #d8e6ff;
            border-radius: 12px;
            background: #ffffff;
        }

        [data-testid="stExpander"] {
            border: 1px solid #d9e7ff;
            border-radius: 10px;
            background: #ffffff;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def ensure_upload_dir(base_dir: str) -> Path:
    upload_dir = Path(base_dir) / "data" / ".streamlit_uploads"
    upload_dir.mkdir(parents=True, exist_ok=True)
    return upload_dir

import base64

def render_pdf_viewer(pdf_path: str):
    with open(pdf_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode("utf-8")

    pdf_display = f"""
        <iframe 
            src="data:application/pdf;base64,{base64_pdf}" 
            width="100%" 
            height="600px" 
            type="application/pdf"
            style="border-radius:10px;"
        ></iframe>
    """
    st.markdown(pdf_display, unsafe_allow_html=True)


def persist_uploaded_pdf(upload_dir: Path, filename: str, content: bytes) -> str:
    file_hash = hashlib.sha256(content).hexdigest()[:16]
    output_path = upload_dir / f"{file_hash}_{filename}"
    output_path.write_bytes(content)
    return str(output_path)


def render_chunks(chunks: list[str]) -> None:
    with st.expander("Retrieved context chunks", expanded=False):
        for idx, chunk in enumerate(chunks, start=1):
            st.markdown(f"**Chunk {idx}**")
            st.write(chunk)
