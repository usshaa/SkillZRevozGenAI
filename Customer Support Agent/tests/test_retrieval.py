import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from retrieval.sparse_retriever import SparseRetriever

def test_sparse_retriever():
    retriever = SparseRetriever()
    docs = ["This is a test document about refund policy.", "How to reset your password."]
    metadatas = [{"doc_id": "1"}, {"doc_id": "2"}]
    retriever.add_documents(docs, metadatas)
    
    results = retriever.search("refund", k=1)
    assert len(results) == 1
    assert results[0]["metadata"]["doc_id"] == "1"
