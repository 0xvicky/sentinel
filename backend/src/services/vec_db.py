from src.schema.schema import ChunkModel
from src.db.qdrant import qdrant_init
from typing import List


def vector_store(chunks: List[ChunkModel], session_id: str):
    """Embed in VectorDB & BM25 Indexing"""

    # embed in vector db
    qdrant_init(chunks, session_id)
    # if success from vector db
    
    # index chunks in postgre

    # if failed in postgre, rollback the vector db data aswell
    pass
