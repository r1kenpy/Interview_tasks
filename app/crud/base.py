from typing import Generic, TypeVar

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base


ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Базовый уруд для остольныз моделей."""

    def __init__(self, model):
        self.model = model

    async def get_multi(self, session: AsyncSession) -> list[ModelType]:
        all_obj = await session.execute(select(self.model))
        return all_obj.scalars().all()

    async def get_by_id(self, session: AsyncSession, id: int) -> ModelType:
        db_obj = await session.execute(
            select(self.model).where(self.model.id == id)
        )
        return db_obj.scalars().first()

    async def create(
        self, session: AsyncSession, obj_data: CreateSchemaType, question_id
    ) -> ModelType:
        obj_data = obj_data.model_dump(exclude_none=True)
        obj_data['question_id'] = question_id
        new_obj_db = self.model(**obj_data)
        session.add(new_obj_db)
        await session.commit()
        await session.refresh(new_obj_db)
        return new_obj_db
