from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from app.crud.base import CRUDBase
from app.crud.block import block_crud
from app.models.answer import Answer
from app.models.association import Association
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
                joinedload(self.model.answers),
                selectinload(self.model.blocks).options(
                    joinedload(Association.block)
                ),
            )
        )
        return all_obj.scalars().unique().all()

    async def get_by_id_v2(self, session: AsyncSession, id: int) -> Question:
        db_obj = await session.execute(
            select(self.model)
            .where(self.model.id == id)
            .options(
                joinedload(self.model.answers),
                selectinload(self.model.blocks).options(
                    joinedload(Association.block)
                ),
            )
        )
        return db_obj.scalars().first()

    async def create_v2(
        self,
        session: AsyncSession,
        obj_data: QuestionCreate,
    ) -> Question:
        data = obj_data.model_dump(exclude_none=True)
        data_answer = data.pop('answers')
        data_blocks = data.pop('blocks')
        print(data)
        new_question = self.model(**data)
        for answer in data_answer:
            new_question.answers.append(Answer(**answer))

        for block in data_blocks:
            block_for_assoc = await block_crud.get_by_title(
                session, block.get('title')
            )
            if block_for_assoc is None:
                block_for_assoc = Block(**data_blocks[0])

            new_question.blocks.append(Association(block=block_for_assoc))

        session.add(new_question)
        await session.commit()
        await session.refresh(new_question)
        return new_question


question_crud = CRUDQuestion(Question)
