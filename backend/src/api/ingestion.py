from fastapi import APIRouter, UploadFile, File
from src.services.store_docs import store
from typing import List
import uuid

router = APIRouter()


@router.api_route("/ingest", methods=["POST"])
async def ingest(files: List[UploadFile] = File(...)):
    print("ingestions")
    session_id = uuid.uuid4()
    # store files in local system
    doc_ids = await store(files, session_id=session_id)

    for id in doc_ids:
        print(id)
    # enqueue the metadata to the queue

    return {"session": session_id, "docs": doc_ids}
