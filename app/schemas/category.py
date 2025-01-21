from pydantic import BaseModel, Field


class CategoryCreate(BaseModel):
    title: str = Field(..., max_length=256)


class CategoryDB(CategoryCreate):
    id: int


class CategoryUpdate(CategoryCreate): ...
