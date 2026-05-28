from src.repository import get_doc
from celery.utils.log import get_task_logger
import pymupdf

logger = get_task_logger(__name__)


def parse_doc(doc_path: str):
    doc = pymupdf.open(doc_path)


def process(doc_id: str):
    doc_metadata = get_doc(doc_id)
    # access that file first
    doc_path = doc_metadata.file_path
    # logger.info(f"Here in process service:{doc_path}")
    # parse the document using pymupdf
    chunks = parse_doc(doc_path)
    # log to see what you're getting
    for i, chunk in enumerate(chunks):
        logger.info(f"Chunk {i} | Section: {chunk['metadata']['section']}")
        logger.info(f"Text preview: {chunk['text'][:100]}")

    logger.info(f"Total chunks: {len(chunks)}")
    
    # ingest it to vector db && bm25 indexing in postgres

    # if success, update the status to ready for query
