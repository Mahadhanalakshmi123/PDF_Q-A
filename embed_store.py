from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class EmbedStore:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = None
        self.chunks = []

    def build(self, chunks):
        self.chunks = chunks
        embeddings = self.model.encode(chunks)
        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(np.array(embeddings))

    def query(self, query, top_k=3):
        if self.index is None:
            return []
        query_vec = self.model.encode([query])
        D, I = self.index.search(np.array(query_vec), top_k)
        return [self.chunks[i] for i in I[0]]
