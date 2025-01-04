from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Answer(BaseModel):
    content: str
    difficulty: str | None


class Block(BaseModel):
    title: str = Field(..., max_length=256)
    level: Optional[int] = Field(None, ge=1)


class QuestionDB(BaseModel):
    id: int
    title: str = Field(..., max_length=256)
    additional: Optional[str] = None
    answers: Optional[list[Answer]] = None
    blocks: Optional[list[Block]] = None
    created_at: datetime
    interview_count: int = Field(..., ge=0)
    time_decision: int = Field(..., ge=0)


class QuestionCreate(BaseModel):
    title: str
    additional: Optional[str] = Field(None, max_length=256)
    answers: Optional[list[Answer]] = None
    blocks: Optional[list[Block]] = None
    time_decision: int = Field(..., ge=1)


class QuestionUpdate(QuestionCreate): ...
