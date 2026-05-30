from qdrant_client import QdrantClient, models
from src.schema.schema import ChunkModel
from typing import List


def qdrant_init(chunks: List[ChunkModel], session_id: str):
    client = QdrantClient(url="http://localhost:6333")

    model_name = "BAAI/bge-small-en"
    # create collecion if not exist
    if not client.collection_exists(collection_name=session_id):
        client.create_collection(
            collection_name=session_id,
            vectors_config=models.VectorParams(
                size=client.get_embedding_size(model_name),
                distance=models.Distance.COSINE,
            ),  # size and distance are model dependent
        )

    # chunk metadata
    metadata_with_docs = [
        {
            "document": chunk.content,
            "metadata": {
                "chunk_id": chunk.chunk_id,
                "doc_id": chunk.doc_id,
                "doc_path": chunk.doc_path,
            },
        }
        for chunk in chunks
    ]
    ids = [chunk.chunk_id for chunk in chunks]
    res = client.upload_collection(
        collection_name=session_id,
        vectors=[
            models.Document(text=chunk.content, model=model_name) for chunk in chunks
        ],
        payload=metadata_with_docs,
        ids=ids,
    )
    print(res)
