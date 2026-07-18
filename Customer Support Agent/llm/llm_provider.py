import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config.settings import GROQ_API_KEY, GROQ_MODEL

def get_llm():
    """Factory returning a LangChain ChatGroq model."""
    from langchain_groq import ChatGroq
    if not GROQ_API_KEY or GROQ_API_KEY == "your_free_groq_key_here":
        raise ValueError("GROQ_API_KEY is not set properly. Please set it in .env")
        
    return ChatGroq(
        api_key=GROQ_API_KEY,
        model_name=GROQ_MODEL,
        temperature=0.0
    )
