from fastapi import APIRouter, UploadFile, File
from typing import List

router = APIRouter()


@router.api_route("/ingest", methods=["POST"])
async def ingest(files: List[UploadFile] = File(...)):
    print("ingestions")
    # print(type (files))
    for file in files:
        print(file)
    return {"ok": "ok"}
