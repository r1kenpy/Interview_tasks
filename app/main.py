from fastapi import FastAPI

from app.api.question import router as question_router
from app.core.config import settings
from app.pages.question import router as question_page_router

app = FastAPI(title=settings.title_app)


app.include_router(question_router)
app.include_router(question_page_router)
