from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Difficulty(BaseModel):
    id: int
    title: str


class Answer(BaseModel):
    content: str
    difficulty: str


class AnswerDB(BaseModel):
    content: str
    difficulty: Difficulty


class Block(BaseModel):
    id: Optional[int] = None
    title: str = Field(..., max_length=256)
    level: Optional[int] = Field(None, ge=1)


class Assoc(BaseModel):
    block: Block


class Category(BaseModel):
    title: str = Field(..., max_length=256)


class QuestionDB(BaseModel):
    id: int
    title: str = Field(..., max_length=256)
    additional: Optional[str] = None
    text_question: str
    answers: Optional[list[AnswerDB]] = None
    category: Optional[Category] = None
    blocks: Optional[list[Assoc]] = None
    created_at: datetime
    interview_count: Optional[int] = Field(None, ge=0)
    time_decision: Optional[int] = Field(None, ge=0)


class QuestionCreate(BaseModel):
    title: str
    additional: Optional[str] = None
    text_question: str
    answers: Optional[list[Answer]] = None
    category: Optional[Category] = None
    blocks: Optional[list[Block]] = None
    time_decision: Optional[int] = Field(None, ge=1)
    interview_count: Optional[int] = Field(None, ge=0)


class QuestionUpdate(QuestionCreate): ...
