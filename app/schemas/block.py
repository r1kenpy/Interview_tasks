from typing import Optional

from pydantic import BaseModel


class BlockDB(BaseModel):
    id: str
    title: str
    level: int
    question: int


class BlockCreate(BaseModel):
    title: str
    level: Optional[int]
    question: Optional[int]


class BlockUpdate(BlockCreate): ...
