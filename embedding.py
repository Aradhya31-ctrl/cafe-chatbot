from sentence_transformers import SentenceTransformer
import faiss, numpy as np

class EmbeddingRetriever:
    def __init__(self, documents, model_name: str = 'sentence-transformers/all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.documents = documents
        self.texts = [d["text"] for d in documents]
        self.ids = [d["id"] for d in documents]
        self.index = None
        self._build_index()

    def _build_index(self):
        embs = self.model.encode(self.texts, convert_to_numpy=True, normalize_embeddings=True)
        dim = embs.shape[1]
        self.index = faiss.IndexFlatIP(dim)  # cosine via normalized dot product
        self.index.add(embs.astype('float32'))
        self.embs = embs

    def retrieve(self, query: str, top_k: int = 5):
        q = self.model.encode([query], convert_to_numpy=True, normalize_embeddings=True).astype('float32')
        scores, idxs = self.index.search(q, top_k)
        results = []
        for rank, i in enumerate(idxs[0]):
            if i < 0: 
                continue
            results.append({
                "id": self.ids[i],
                "text": self.texts[i],
                "score": float(scores[0][rank])
            })
        return results
