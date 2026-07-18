import os
from dotenv import load_dotenv

load_dotenv()

# LLM
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

# Embeddings
EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "huggingface")
HF_EMBEDDING_MODEL = os.getenv("HF_EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

# Vector store
VECTOR_STORE = os.getenv("VECTOR_STORE", "qdrant")
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
VECTORSTORE_PATH = os.getenv("VECTORSTORE_PATH", "data/vectorstore")

# Chunking
CHUNKING_STRATEGY = os.getenv("CHUNKING_STRATEGY", "character")

# Deduplication
DEDUP_ENABLED = os.getenv("DEDUP_ENABLED", "true").lower() == "true"
DEDUP_HASH_ALGO = os.getenv("DEDUP_HASH_ALGO", "sha256")

# Hybrid retrieval
RETRIEVAL_STRATEGY = os.getenv("RETRIEVAL_STRATEGY", "hybrid")
RRF_K = int(os.getenv("RRF_K", "60"))

# Reranking
RERANK_PROVIDER = os.getenv("RERANK_PROVIDER", "local")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
LOCAL_RERANK_MODEL = os.getenv("LOCAL_RERANK_MODEL", "cross-encoder/ms-marco-MiniLM-L-6-v2")

# Memory
SHORT_TERM_STRATEGY = os.getenv("SHORT_TERM_STRATEGY", "summarize")
SHORT_TERM_MAX_TOKENS = int(os.getenv("SHORT_TERM_MAX_TOKENS", "3000"))
LONG_TERM_MEMORY_ENABLED = os.getenv("LONG_TERM_MEMORY_ENABLED", "true").lower() == "true"
LONG_TERM_STORE_PATH = os.getenv("LONG_TERM_STORE_PATH", "data/memory_store/novashop_memory.db")

# Structured data
DB_PROVIDER = os.getenv("DB_PROVIDER", "sqlite")
SQLITE_DB_PATH = os.getenv("SQLITE_DB_PATH", "data/generated/novashop.db")
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
MYSQL_DB = os.getenv("MYSQL_DB", "novashop")
MYSQL_USER = os.getenv("MYSQL_USER", "novashop_user")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")

# Observability
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2", "false").lower() == "true"
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT", "novashop-support-agent")
