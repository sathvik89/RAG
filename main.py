from rag.embed import embedder, reranker
from rag.utils import extract_text_from_pdf, chunk_text
from rag.store import create_faiss_index
from rag.retrieve import retrieve
from rag.generate import generate_answer


def setup_rag():
    print("Loading document...")

    pdf_path = 'data/deep-learning.pdf'

    text = extract_text_from_pdf(pdf_path)
    docs = chunk_text(text)

    print(f"Chunks created: {len(docs)}")
    print("Generating embeddings...")

    doc_embeddings = embedder.encode(docs)
    index = create_faiss_index(doc_embeddings)

    print("System ready.\n")

    return docs, index


def chat_loop(docs, index):
    print("Enter your question (type 'exit' to quit)\n")
    while True:
        query = input("You: ").strip()

        if query.lower() in ("exit", "quit"):
            print("Exiting...")
            break

        if not query:
            print("Please enter a valid question.\n")
            continue

        print("Retrieving relevant context...")
        best_docs = retrieve(query, embedder, index, docs, reranker)

        print("Generating answer...\n")

        answer = generate_answer(query, best_docs)
        
        print("Answer:")
        print(answer)
        print("-" * 50)


if __name__ == '__main__':
    docs, index = setup_rag()
    chat_loop(docs, index)