import os
import sys
import glob
import uuid
from datetime import datetime
import re

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from ingestion.dedup import compute_content_hash
from ingestion.metadata_schema import ChunkMetadata
from ingestion.chunking_strategies import get_character_splitter, get_semantic_splitter
from config.settings import CHUNKING_STRATEGY

def load_and_chunk_documents():
    faq_docs_dir = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "faq_docs")
    files = glob.glob(os.path.join(faq_docs_dir, "*.md"))
    
    chunks_with_metadata = []
    
    if CHUNKING_STRATEGY == "semantic":
        splitter = get_semantic_splitter()
    else:
        splitter = get_character_splitter()

    for file_path in files:
        filename = os.path.basename(file_path)
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        doc_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, filename))
        
        chunks = splitter.split_text(content)
        for i, chunk in enumerate(chunks):
            # Compute hash first so we can use it for the deterministic UUID
            chash = compute_content_hash(chunk)
            chunk_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, chash))
            
            section_title = None
            headings = re.findall(r'^#+\s+(.*)', chunk, re.MULTILINE)
            if headings:
                section_title = headings[0]
                
            meta = ChunkMetadata(
                doc_id=doc_id,
                source_file=filename,
                chunk_id=chunk_id,
                chunk_index=i,
                chunking_strategy=CHUNKING_STRATEGY,
                content_hash=chash,
                section_title=section_title,
                created_at=datetime.now().isoformat()
            )
            chunks_with_metadata.append({"text": chunk, "metadata": meta.model_dump()})
                
    return chunks_with_metadata

from embeddings.vector_store import get_vector_store
from retrieval.sparse_retriever import SparseRetriever

if __name__ == "__main__":
    chunks = load_and_chunk_documents()
    print(f"Loaded and chunked {len(chunks)} chunks using {CHUNKING_STRATEGY} strategy.")
    
    # Extract texts and metadatas
    texts = [c["text"] for c in chunks]
    metadatas = [c["metadata"] for c in chunks]
    
    # 1. Save to Qdrant (Dense Vector Store)
    print("Saving to Qdrant Vector Store...")
    from embeddings.vector_store import get_qdrant_client, COLLECTION_NAME
    from embeddings.embedding_service import get_embedding_model
    
    client = get_qdrant_client()
    if not client.collection_exists(COLLECTION_NAME):
        print(f"Collection {COLLECTION_NAME} doesn't exist. Creating...")
        from qdrant_client.models import VectorParams, Distance
        # Get embedding dimension dynamically
        emb_model = get_embedding_model()
        dim = len(emb_model.embed_query("test dimension"))
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=dim, distance=Distance.COSINE)
        )
        
    qdrant = get_vector_store()
    ids = [c["metadata"]["chunk_id"] for c in chunks]
    qdrant.add_texts(texts=texts, metadatas=metadatas, ids=ids)
    
    # 2. Save to BM25 (Sparse Vector Store)
    print("Saving to BM25 Sparse Store...")
    bm25 = SparseRetriever()
    bm25.add_documents(documents=texts, metadatas=metadatas)
    
    print("Ingestion complete!")
