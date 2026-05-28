from src.db.db import get_db_conn
from src.schema.schema import FileModel
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


def get_doc(doc_id: str) -> FileModel:
    try:
        with get_db_conn() as conn:
            with conn.cursor() as cursor:
                get_doc_query = """
                SELECT doc_id, storage_path,doc_size,doc_name,session_id FROM documents WHERE doc_id=%s
                """
                query_data = (doc_id,)
                cursor.execute(get_doc_query, query_data)
                res = cursor.fetchone()
                if res != None:
                    print(res)
                    logger.info(res)
                    # logger.info(f"🚀 TASK Fetched: process_worker received doc_id: {res}")
                    return FileModel(
                        file_id=res[0],
                        file_path=res[1],
                        file_size=res[2],
                        file_name=res[3],
                        session_id=res[4],
                    )
                else:
                    logger.info("No res found")
    except Exception as e:
        print(f"Error occured while fetching doc:{e}")
