import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config.settings import HF_EMBEDDING_MODEL

def get_embedding_model():
    """Returns HuggingFaceEmbeddings."""
    from langchain_community.embeddings import HuggingFaceEmbeddings
    return HuggingFaceEmbeddings(model_name=HF_EMBEDDING_MODEL)
