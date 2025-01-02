from datetime import datetime
from typing import Optional, Union


from pydantic import BaseModel, Field


class QuestionDB(BaseModel):
    id: int
    title: str
    additional: str
    answer_id: Union[int, list[int]]
    block_id: Union[int, list[int]]
    created_at: datetime
    interview_count: int
    time_decision: int


class QuestionCreate(BaseModel):
    title: str
    additional: str
    answer_id: Union[int, list[int]]
    block_id: Union[int, list[int]]
    created_at: datetime = Field(..., default_factory=datetime.now)
    interview_count: int
    time_decision: int


class QuestionUpdate(QuestionCreate): ...
