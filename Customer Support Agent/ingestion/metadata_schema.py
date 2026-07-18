from pydantic import BaseModel
from typing import Optional

class ChunkMetadata(BaseModel):
    doc_id: str
    source_file: str
    chunk_id: str
    chunk_index: int
    parent_id: Optional[str] = None
    chunking_strategy: str
    content_hash: str
    section_title: Optional[str] = None
    created_at: str
