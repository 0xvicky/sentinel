from celery import Celery
from src.services.process_docs import process

celery_app = Celery(
    "sentinel-worker", broker="redis://localhost:6379/0", include=["src.worker"]
)


@celery_app.task
def process_worker(doc_id: str):
    print("in process worker", flush=True)
    res = process(doc_id)
    return res