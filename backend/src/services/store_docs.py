from fastapi import UploadFile
from typing import List
from pathlib import Path
from src.schema.schema import FileModel
from src.db.db import get_db_conn
import uuid

# put the session to doc mapping in redis


async def store_docs(doc: FileModel):
    type(doc.file_path)
    try:
        with get_db_conn() as conn:
            with conn.cursor() as cursor:
                doc_insert_qry = """
                INSERT INTO documents(
                    doc_id, storage_path, doc_size, doc_name, session_id
                ) VALUES (%s, %s, %s, %s,%s);
                """
                record_values = (
                    doc.file_id,
                    doc.file_path,
                    doc.file_size,
                    doc.file_name,
                    doc.session_id,
                )
                cursor.execute(doc_insert_qry, record_values)
                print("doc recorded success")
    except Exception as e:
        print(f"{e}")
    return


async def store(files: List[UploadFile], session_id: uuid.UUID):
    doc_ids = []
    # create temp folder if not exist and then sub folder for session
    path = Path(f"/mnt/data/Code/ai-projects/sentinel/tmp/{session_id}")
    path.mkdir(parents=True, exist_ok=True)
    # store each file into that folder
    for file in files:
        try:
            id = uuid.uuid4()
            file_dest = path / file.filename
            file_dest.write_bytes(await file.read())
            file_model = FileModel(
                file_id=str(id),
                file_path=str(file_dest),
                session_id=str(session_id),
                file_size=file.size,
                file_name=file.filename,
            )
            doc_ids.append(file_model.file_id)
            await store_docs(doc=file_model)
        except Exception as e:
            print(f"{e}")
    return doc_ids
