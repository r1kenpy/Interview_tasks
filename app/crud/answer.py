from app.crud.base import CRUDBase
from app.models.answer import Answer
from app.schemas.answer import AnswerCreate, AnswerUpdate
from sqlalchemy.orm import lazyload, joinedload

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class CRUDAnswer(CRUDBase[Answer, AnswerCreate, AnswerUpdate]):

    async def get_multi_with_question(
        self, session: AsyncSession
    ) -> list[Answer]:
        all_obj = await session.execute(
            select(self.model).options(joinedload(self.model.question_answers))
        )
        return all_obj.scalars().all()


answer_crud = CRUDAnswer(Answer)
