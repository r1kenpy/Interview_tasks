from typing import Optional

from pydantic import BaseModel, Field


class BlockDB(BaseModel):
    id: int
    title: str
    level: Optional[int] = None
    question_id: int


class BlockCreate(BaseModel):
    title: str = Field(..., max_length=256)
    level: Optional[int] = Field(None, ge=1)
    question_id: int = Field(..., ge=1)


class BlockUpdate(BlockCreate): ...
