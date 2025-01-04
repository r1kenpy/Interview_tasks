from typing import Optional

from pydantic import BaseModel, Field

from app.schemas.question import QuestionDB


class AnswerDB(BaseModel):
    id: int
    content: str
    difficulty: str
    question: Optional[QuestionDB] = None


class AnswerCreate(BaseModel):
    content: str
    difficulty: str = Field(..., max_length=256)  # Enum or model?


class AnswerUpdate(AnswerCreate): ...
