from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(title=settings.title_app)
