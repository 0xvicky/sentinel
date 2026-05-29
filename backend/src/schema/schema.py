from pydantic import BaseModel
from pathlib import Path


class FileModel(BaseModel):
    file_id: str
    file_path: str
    file_size: int
    file_name: str
    session_id: str


class ChunkModel(BaseModel):
    chunk_id:int
    content:str
    doc_id:str
    doc_path:str