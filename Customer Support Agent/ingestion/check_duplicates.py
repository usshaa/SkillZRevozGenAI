import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from embeddings.vector_store import get_qdrant_client, COLLECTION_NAME
from retrieval.sparse_retriever import SparseRetriever

def check_duplicates():
    client = get_qdrant_client()
    
    if not client.collection_exists(COLLECTION_NAME):
        print("Collection does not exist.")
        return

    # Scroll through all points in Qdrant
    points, _ = client.scroll(
        collection_name=COLLECTION_NAME,
        limit=10000,
        with_payload=True
    )
    
    print(f"Total points in Qdrant: {len(points)}")
    
    # Check for duplicate content_hashes
    hash_counts = {}
    for point in points:
        metadata = point.payload.get("metadata", {})
        chash = metadata.get("content_hash")
        if chash:
            hash_counts[chash] = hash_counts.get(chash, 0) + 1
            
    duplicates = {k: v for k, v in hash_counts.items() if v > 1}
    print(f"Number of unique hashes: {len(hash_counts)}")
    print(f"Number of duplicated hashes: {len(duplicates)}")
    
    if duplicates:
        print("\nFound duplicates!")
        for chash, count in list(duplicates.items())[:5]:
            print(f"Hash {chash[:10]}... appears {count} times.")
    
    print("\n--- BM25 Index ---")
    bm25 = SparseRetriever()
    print(f"Total documents in BM25: {len(bm25.corpus)}")

if __name__ == "__main__":
    check_duplicates()
