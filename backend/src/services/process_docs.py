from src.repository import get_doc
from celery.utils.log import get_task_logger
import fitz
import pymupdf
from src.schema.schema import ChunkModel, FileModel
from typing import List

logger = get_task_logger(__name__)

# separator = ["\n\n", "\n", ".", ""]


def chunker(cln_txt: str, doc_metadata: FileModel):
    CHUNK_SIZE = 500
    OVERLAP = 50
    STRIDE = CHUNK_SIZE - OVERLAP
    i = 0
    chunks: List[ChunkModel] = []
    idx = 0

    while i < len(cln_txt):
        chunk_content = (
            cln_txt[i:]
            if len(cln_txt) - i < CHUNK_SIZE
            else cln_txt[i : i + CHUNK_SIZE]
        )
        chunk = ChunkModel(
            chunk_id=idx,
            content=chunk_content,
            doc_id=doc_metadata.file_id,
            doc_path=doc_metadata.file_path,
        )
        chunks.append(chunk)
        i += STRIDE
        idx += 1

    return chunks


def extract(doc_path: str):
    """Extract the content from the whole document"""
    cleaned_data = ""

    with fitz.open(doc_path) as doc:
        for page_num in range(len(doc)):
            # load_page
            page = doc.load_page(page_num)
            # clean the text
            blocks = page.get_text("blocks")
            for block in blocks:
                text = block[4]
                cleaned_data += text
            # chunk the text based on certain strategy

    return cleaned_data


def parse_doc(doc_metadata: FileModel):
    """Return chunks from the document for ingestion."""
    # extract the cleaned data from doc
    doc_path = doc_metadata.file_path
    logger.info("Here it is")
    clean_data = extract(doc_path)
    # print(clean_data)
    # recursive chunking
    ch = chunker(clean_data, doc_metadata)

    return ch


def process(doc_id: str):
    """Process each doc for vectorDB ingestion."""
    doc_metadata = get_doc(doc_id)
    # access that file first
    # logger.info(f"Here in process service:{doc_path}")
    # parse the document using pymupdf
    chunks = parse_doc(doc_metadata)
    # log to see what you're getting
    logger.info(chunks)
    # ingest it to vector db && bm25 indexing in postgres

    # if success, update the status to ready for query
