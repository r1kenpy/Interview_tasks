from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.crud.base import CRUDBase
from app.models.answer import Answer
from app.models.block import Block
from app.models.question import Question
from app.schemas.question import QuestionCreate, QuestionUpdate


class CRUDQuestion(CRUDBase[Question, QuestionCreate, QuestionUpdate]):

    async def get_by_id_with_answer(
        self, session: AsyncSession, id: int
    ) -> Question:
        db_obj = await session.execute(
            select(self.model)
            .where(self.model.id == id)
            .options(
                joinedload(self.model.answers),
                joinedload(self.model.blocks),
            )
        )
        return db_obj.scalars().first()

    async def get_multi_v2(self, session: AsyncSession) -> list[Question]:
        all_obj = await session.execute(
            select(self.model).options(
                joinedload(self.model.answers), joinedload(self.model.blocks)
            )
        )
        return all_obj.scalars().unique().all()

    async def create_v2(
        self,
        session: AsyncSession,
        obj_data: QuestionCreate,
    ) -> tuple[Question, dict[str, Any]]:
        obj_data = obj_data.model_dump(exclude_none=True)
        answers = obj_data.pop('answers')
        blocks = obj_data.pop('blocks')
        new_obj_in_db = self.model(**obj_data)
        for answer in answers:
            new_obj_in_db.answers.append(Answer(**answer))
        for block in blocks:
            new_obj_in_db.blocks.append(Block(**block))
        session.add(new_obj_in_db)
        await session.commit()
        await session.refresh(new_obj_in_db)
        return new_obj_in_db


question_crud = CRUDQuestion(Question)
