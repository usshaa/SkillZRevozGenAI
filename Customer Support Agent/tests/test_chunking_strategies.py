import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from ingestion.chunking_strategies import get_character_splitter, get_parent_splitter, get_child_splitter

def test_character_splitter():
    splitter = get_character_splitter()
    text = "A" * 1000
    chunks = splitter.split_text(text)
    assert len(chunks) > 1
    assert len(chunks[0]) <= 500

def test_parent_child_splitter():
    parent_splitter = get_parent_splitter()
    child_splitter = get_child_splitter()
    text = "B" * 3000
    parents = parent_splitter.split_text(text)
    assert len(parents) > 1
    
    children = child_splitter.split_text(parents[0])
    assert len(children) > 1
