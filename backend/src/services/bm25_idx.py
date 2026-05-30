from typing import List
from src.schema.schema import ChunkModel
from rank_bm25 import BM25Okapi


def bm25_index(chunks: List[ChunkModel]):
    tokenized_idxs = [chunk.content.lower().split() for chunk in chunks]
    bm25 = BM25Okapi(tokenized_idxs)
    return bm25


def bm25_search(chunks, bm25_search):
    pass
