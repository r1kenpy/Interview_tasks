from typing import Optional

from pydantic import BaseModel


class AnswerDB(BaseModel):
    id: int
    content: Optional[str]
    difficulty: Optional[str]
    question: Optional[int]


class AnswerCreate(BaseModel):
    content: str
    difficulty: str  # Enum or model?
    question: Optional[int]


class AnswerUpdate(AnswerCreate): ...
