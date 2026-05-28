from fastapi import APIRouter, UploadFile, File
from src.services.store_docs import store
from src.worker import process_worker
from typing import List
import uuid
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)
router = APIRouter()


@router.api_route("/ingest", methods=["POST"])
async def ingest(files: List[UploadFile] = File(...)):
    print("ingestions")
    session_id = uuid.uuid4()
    # store files in local system
    doc_ids = await store(files, session_id=session_id)

    for id in doc_ids:
        # enqueue the metadata to the queue
        task = process_worker.delay(doc_id=id)
        print("here in enqueue")
        print(task)

    return {"session": session_id, "docs": doc_ids}
