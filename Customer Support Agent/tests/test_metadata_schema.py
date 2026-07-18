import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import pytest
from pydantic import ValidationError
from ingestion.metadata_schema import ChunkMetadata
from datetime import datetime

def test_valid_metadata():
    data = {
        "doc_id": "doc123",
        "source_file": "file.md",
        "chunk_id": "chunk1",
        "chunk_index": 0,
        "chunking_strategy": "character",
        "content_hash": "abc123hash",
        "created_at": datetime.now().isoformat()
    }
    meta = ChunkMetadata(**data)
    assert meta.doc_id == "doc123"
    assert meta.parent_id is None

def test_missing_required_field():
    data = {
        "doc_id": "doc123"
    }
    with pytest.raises(ValidationError):
        ChunkMetadata(**data)
