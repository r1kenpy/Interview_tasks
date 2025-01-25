from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, load_only

from app.crud.base import CRUDBase
from app.models.answer import Answer
from app.schemas.answer import AnswerCreate, AnswerUpdate


class CRUDAnswer(CRUDBase[Answer, AnswerCreate, AnswerUpdate]):

    async def get_multi_with_question(
        self, session: AsyncSession
    ) -> list[Answer]:
        all_obj = await session.execute(
            select(self.model).options(joinedload(self.model.question_answers))
        )
        return all_obj.scalars().all()

    async def get_all_difficulty(self, session: AsyncSession) -> list[Answer]:
        dif = await session.execute(
            select(self.model)
            .distinct()
            .options(
                load_only(
                    self.model.difficulty,
                )
            )
        )
        return dif.scalars().unique().all()


answer_crud = CRUDAnswer(Answer)
