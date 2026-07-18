import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from retrieval.hybrid_retriever import reciprocal_rank_fusion

def test_rrf():
    sparse_results = [
        {"metadata": {"chunk_id": "docA"}, "text": "A"},
        {"metadata": {"chunk_id": "docB"}, "text": "B"}
    ]
    dense_results = [
        {"metadata": {"chunk_id": "docB"}, "text": "B"},
        {"metadata": {"chunk_id": "docC"}, "text": "C"}
    ]
    
    fused = reciprocal_rank_fusion(sparse_results, dense_results, k=60)
    
    assert len(fused) == 3
    # docB should be ranked first since it is in both top 2
    assert fused[0]['metadata']['chunk_id'] == "docB"
    assert 'rrf_score' in fused[0]
