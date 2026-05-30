from src.schema.schema import ChunkModel
from src.db.qdrant import qdrant_init
from src.services.bm25_idx import bm25_index
from typing import List
from src.cache.cache import BM25_REGISTRY


def vector_store(chunks: List[ChunkModel], session_id: str):
    """Embed in VectorDB & BM25 Indexing"""

    # embed in vector db
    qdrant_init(chunks, session_id)
    # if success from vector db index chunks to bm25
    return True
