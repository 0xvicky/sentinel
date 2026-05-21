from fastapi import FastAPI
from src.api import health, ingestion

app = FastAPI()


app.include_router(health.router)
app.include_router(ingestion.router)
