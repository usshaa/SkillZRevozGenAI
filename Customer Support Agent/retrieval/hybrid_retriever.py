import os
import sys
from typing import List, Dict

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config.settings import RRF_K

def reciprocal_rank_fusion(sparse_results: List[Dict], dense_results: List[Dict], k: int = RRF_K) -> List[Dict]:
    """Combines sparse and dense results using Reciprocal Rank Fusion."""
    fused_scores = {}
    docs_map = {}
    
    # Process sparse results
    for rank, res in enumerate(sparse_results):
        doc_id = res['metadata']['chunk_id']
        docs_map[doc_id] = res
        fused_scores[doc_id] = fused_scores.get(doc_id, 0) + 1.0 / (rank + k)
        
    # Process dense results
    for rank, res in enumerate(dense_results):
        doc_id = res['metadata']['chunk_id']
        if doc_id not in docs_map:
            docs_map[doc_id] = res
        fused_scores[doc_id] = fused_scores.get(doc_id, 0) + 1.0 / (rank + k)
        
    # Sort by fused score
    sorted_docs = sorted(fused_scores.items(), key=lambda x: x[1], reverse=True)
    
    # Return formatted results
    final_results = []
    for doc_id, score in sorted_docs:
        doc_info = docs_map[doc_id].copy()
        doc_info['rrf_score'] = score
        final_results.append(doc_info)
        
    return final_results
