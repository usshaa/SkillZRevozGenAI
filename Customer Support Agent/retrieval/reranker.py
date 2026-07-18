import os
import sys
from typing import List, Dict

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config.settings import RERANK_PROVIDER, COHERE_API_KEY, LOCAL_RERANK_MODEL

class RerankerService:
    def __init__(self):
        self.provider = RERANK_PROVIDER.lower()
        if self.provider == "cohere":
            if not COHERE_API_KEY:
                raise ValueError("COHERE_API_KEY is not set.")
            import cohere
            self.cohere_client = cohere.Client(COHERE_API_KEY)
        else:
            from sentence_transformers import CrossEncoder
            self.model = CrossEncoder(LOCAL_RERANK_MODEL)
            
    def rerank(self, query: str, documents: List[Dict], top_n: int = 5) -> List[Dict]:
        if not documents:
            return []
            
        texts = [doc['text'] for doc in documents]
        
        if self.provider == "cohere":
            response = self.cohere_client.rerank(
                query=query,
                documents=texts,
                top_n=top_n,
                model='rerank-english-v3.0'
            )
            results = []
            for item in response.results:
                doc = documents[item.index].copy()
                doc['rerank_score'] = item.relevance_score
                results.append(doc)
            return results
        else:
            pairs = [[query, text] for text in texts]
            scores = self.model.predict(pairs)
            
            # Combine scores with docs
            scored_docs = list(zip(documents, scores))
            scored_docs.sort(key=lambda x: x[1], reverse=True)
            
            results = []
            for doc, score in scored_docs[:top_n]:
                new_doc = doc.copy()
                new_doc['rerank_score'] = float(score)
                results.append(new_doc)
            return results
