import numpy as np


def retrieve(query, embedder, index, docs, reranker, initial_k=10, final_k=3):
    query_vector = embedder.encode([query]).astype('float32')
    _, indices = index.search(query_vector, initial_k)

    candidate_docs = [docs[idx] for idx in indices[0]]

    #Reranking for precision
    pairs = [[query, doc] for doc in candidate_docs]
    scores = reranker.predict(pairs)

    ranked_indices = np.argsort(scores)[::-1]
    best_docs = [candidate_docs[i] for i in ranked_indices[:final_k]]

    return best_docs