from fastapi import FastAPI
from src.db.db import db_init
from src.api import health, ingestion
from contextlib import contextmanager

app = FastAPI()

# init db
db_init()

app.include_router(health.router)
app.include_router(ingestion.router)
