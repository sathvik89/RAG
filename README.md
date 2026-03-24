# RAG-based Question Answering on Deep Learning PDF

A Retrieval-Augmented Generation (RAG) pipeline that answers questions based on PDF document content using semantic search and LLM generation.

## Features

- Extract and chunk PDF documents
- Vector embeddings with sentence-transformers
- FAISS-based semantic search
- Cross-encoder reranking for accuracy
- LLM response generation via Groq API
- Simple CLI interface

## Project Structure

```
rag-project/
├── data/
│   └── your.pdf
├── rag/
│   ├── embed.py
│   ├── store.py
│   ├── retrieve.py
│   ├── generate.py
│   └── utils.py
├── main.py
├── requirements.txt
├── .env
└── README.md
```

## Installation

### 1. Clone repository
```bash
git clone https://github.com/your-username/rag-project.git
cd rag-project
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your PDF
Place your document in `data/` folder

### 5. Setup environment
Create `.env` file:
```
GROQ_API_KEY=your_api_key_here
```

## Usage

```bash
python main.py
```

Example:
```
Enter your question: What is deep learning?

Answer: Deep learning is a subset of machine learning...
```

## How It Works

1. **PDF Processing** → Extract text from PDF
2. **Chunking** → Split into overlapping chunks
3. **Embeddings** → Convert to vector representations
4. **FAISS Search** → Find top-K relevant chunks
5. **Reranking** → Improve relevance with cross-encoder
6. **LLM Generation** → Generate final answer

## Tech Stack

- **Embedding Model**: sentence-transformers (all-MiniLM-L6-v2)
- **Vector Store**: FAISS
- **Reranker**: ms-marco-MiniLM-L-6-v2
- **LLM**: Groq LLaMA 3.1

## Limitations

- Embeddings recomputed on each run
- Best with well-structured PDFs
- No persistent vector storage yet

## Future Enhancements

- Persistent FAISS index storage
- FastAPI backend
- React frontend
- Multi-document support
- Hybrid search (BM25 + vectors)

## License

Educational purposes only
