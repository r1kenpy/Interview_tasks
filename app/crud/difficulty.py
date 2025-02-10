from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.difficulty import Difficulty
from app.schemas.difficulty import DifficultyCreate, DifficultyUpdate


class DifficultyCRUD(CRUDBase[Difficulty, DifficultyCreate, DifficultyUpdate]):
    def __init__(self, model):
        self.model = model

    async def get_multi(self, session: AsyncSession) -> list[Difficulty]:
        all_obj = await session.execute(select(self.model).order_by('title'))
        return all_obj.scalars().all()

    async def get_by_title(
        self,
        session: AsyncSession,
        title: str,
    ) -> Difficulty | None:
        obj = await session.execute(
            select(self.model).where(self.model.title == title)
        )
        return obj.scalars().first()


difficulty_crud = DifficultyCRUD(Difficulty)
