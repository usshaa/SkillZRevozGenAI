import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config.settings import QDRANT_URL, VECTORSTORE_PATH
from qdrant_client import QdrantClient
from langchain_qdrant import QdrantVectorStore
from embeddings.embedding_service import get_embedding_model

COLLECTION_NAME = "novashop_faq"

def get_qdrant_client():
    # Attempt to connect to local docker Qdrant
    try:
        client = QdrantClient(url=QDRANT_URL, timeout=2.0)
        # test connection
        client.get_collections()
        return client
    except Exception as e:
        # Fallback to local file-based Qdrant if docker isn't running
        os.makedirs(os.path.dirname(VECTORSTORE_PATH), exist_ok=True)
        return QdrantClient(path=VECTORSTORE_PATH)

def get_vector_store():
    client = get_qdrant_client()
    embeddings = get_embedding_model()
    return QdrantVectorStore(
        client=client,
        collection_name=COLLECTION_NAME,
        embedding=embeddings
    )
