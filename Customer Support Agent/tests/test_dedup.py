import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from ingestion.dedup import normalize_text, compute_content_hash

def test_normalize_text():
    text = "  Hello   World \n This is a test.  "
    assert normalize_text(text) == "hello world this is a test."

def test_compute_content_hash():
    text1 = "Hello World"
    text2 = "hello world"
    text3 = "  Hello   World  "
    
    hash1 = compute_content_hash(text1)
    hash2 = compute_content_hash(text2)
    hash3 = compute_content_hash(text3)
    
    assert hash1 == hash2
    assert hash1 == hash3
