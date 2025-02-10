from pydantic import BaseModel


class DifficultyBase(BaseModel):
    title: str


class DifficultyDB(DifficultyBase):
    id: int


class DifficultyCreate(DifficultyBase): ...


class DifficultyUpdate(DifficultyBase): ...
