from __future__ import annotations

from rag.embed import embedder, reranker
from rag.generate import generate_answer
from rag.retrieve import retrieve
from rag.store import create_faiss_index
from rag.utils import chunk_text, extract_text_from_pdf


def initialize_rag(pdf_path: str):
    text = extract_text_from_pdf(pdf_path)
    if not text or not text.strip():
        raise ValueError("No readable text found in the selected PDF.")

    docs = chunk_text(text)
    if not docs:
        raise ValueError("Unable to create text chunks from the selected PDF.")

    doc_embeddings = embedder.encode(docs)
    index = create_faiss_index(doc_embeddings)
    return docs, index


def answer_query(query: str, docs, index):
    if not query or not query.strip():
        raise ValueError("Question cannot be empty.")

    best_docs = retrieve(
        query=query.strip(),
        embedder=embedder,
        index=index,
        docs=docs,
        reranker=reranker,
    )
    answer = generate_answer(query.strip(), best_docs)
    return answer, best_docs
