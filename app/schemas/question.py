from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Answer(BaseModel):
    content: str
    difficulty: str | None


class Block(BaseModel):
    id: int
    title: str = Field(..., max_length=256)
    level: Optional[int] = Field(None, ge=1)


class Assoc(BaseModel):
    block: Block


class QuestionDB(BaseModel):
    id: int
    title: str = Field(..., max_length=256)
    additional: Optional[str] = None
    text_question: str
    answers: Optional[list[Answer]] = None
    blocks: Optional[list[Assoc]] = None
    created_at: datetime
    interview_count: Optional[int] = Field(None, ge=0)
    time_decision: int = Field(..., ge=0)


class QuestionCreate(BaseModel):
    title: str
    additional: Optional[str] = Field(None, max_length=256)
    answers: Optional[list[Answer]] = None
    blocks: Optional[list[Block]] = None
    time_decision: int = Field(..., ge=1)


class QuestionUpdate(QuestionCreate): ...
