import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_experimental.text_splitter import SemanticChunker
from embeddings.embedding_service import get_embedding_model


def get_character_splitter():
    return RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

def get_semantic_splitter():
    embeddings = get_embedding_model()
    return SemanticChunker(embeddings)
