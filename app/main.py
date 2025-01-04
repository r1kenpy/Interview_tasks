from fastapi import FastAPI
from app.core.config import settings
from app.api.question import router as quesion_router

app = FastAPI(title=settings.title_app)


app.include_router(quesion_router)
