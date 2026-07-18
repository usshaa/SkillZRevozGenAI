import os
import sys
import pickle

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from rank_bm25 import BM25Okapi
from config.settings import VECTORSTORE_PATH

BM25_INDEX_PATH = os.path.join(VECTORSTORE_PATH, "bm25_index.pkl")
CORPUS_PATH = os.path.join(VECTORSTORE_PATH, "bm25_corpus.pkl")

class SparseRetriever:
    def __init__(self):
        self.bm25 = None
        self.corpus = []
        self.metadatas = []
        self._load_index()
        
    def _load_index(self):
        if os.path.exists(BM25_INDEX_PATH) and os.path.exists(CORPUS_PATH):
            with open(BM25_INDEX_PATH, 'rb') as f:
                self.bm25 = pickle.load(f)
            with open(CORPUS_PATH, 'rb') as f:
                data = pickle.load(f)
                self.corpus = data.get('corpus', [])
                self.metadatas = data.get('metadatas', [])
                
    def save_index(self):
        os.makedirs(os.path.dirname(BM25_INDEX_PATH), exist_ok=True)
        with open(BM25_INDEX_PATH, 'wb') as f:
            pickle.dump(self.bm25, f)
        with open(CORPUS_PATH, 'wb') as f:
            pickle.dump({'corpus': self.corpus, 'metadatas': self.metadatas}, f)
            
    def add_documents(self, documents, metadatas):
        # Extract existing hashes to prevent duplicates
        existing_hashes = {m.get("content_hash") for m in self.metadatas if m.get("content_hash")}
        
        new_docs = []
        new_metas = []
        for doc, meta in zip(documents, metadatas):
            chash = meta.get("content_hash")
            if chash not in existing_hashes:
                new_docs.append(doc)
                new_metas.append(meta)
                existing_hashes.add(chash)
                
        if new_docs:
            self.corpus.extend(new_docs)
            self.metadatas.extend(new_metas)
            # Tokenize
            tokenized_corpus = [doc.lower().split() for doc in self.corpus]
            self.bm25 = BM25Okapi(tokenized_corpus)
            self.save_index()
        
    def search(self, query: str, k: int = 5):
        if not self.bm25:
            return []
        tokenized_query = query.lower().split()
        scores = self.bm25.get_scores(tokenized_query)
        
        # Get top k
        top_n = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]
        
        results = []
        for idx in top_n:
            if scores[idx] > 0:
                results.append({
                    "text": self.corpus[idx],
                    "metadata": self.metadatas[idx],
                    "score": scores[idx]
                })
        return results
