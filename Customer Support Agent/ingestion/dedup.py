import hashlib
import re

def normalize_text(text: str) -> str:
    """Lowercases and collapses whitespace."""
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def compute_content_hash(text: str) -> str:
    """Computes SHA-256 of normalized text."""
    normalized = normalize_text(text)
    return hashlib.sha256(normalized.encode('utf-8')).hexdigest()
