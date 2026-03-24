from sentence_transformers import SentenceTransformer, CrossEncoder

print('Loading models...')
embedder = SentenceTransformer('all-MiniLM-L6-v2')
reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')