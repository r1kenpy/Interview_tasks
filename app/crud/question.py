from typing import Any

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.sql.expression import func

from app.crud.base import CRUDBase
from app.crud.block import block_crud
from app.crud.category import category_crud
from app.crud.difficulty import difficulty_crud
from app.models.answer import Answer
from app.models.association import Association
from app.models.block import Block
from app.models.category import Category
from app.models.difficulty import Difficulty
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
                joinedload(self.model.answers).options(
                    joinedload(Answer.difficulty)
                ),
                joinedload(self.model.blocks),
            )
        )
        return db_obj.scalars().first()

    async def get_multy_by_category_id(
        self, session: AsyncSession, category_id: int
    ) -> list[Question]:
        all_questions = await session.execute(
            select(self.model)
            .where(self.model.category_id == category_id)
            .options(
                joinedload(self.model.answers).options(
                    joinedload(Answer.difficulty)
                ),
                selectinload(self.model.blocks).options(
                    joinedload(Association.block)
                ),
            )
        )
        return all_questions.scalars().unique().all()

    async def get_multi_v2(self, session: AsyncSession) -> list[Question]:
        all_obj = await session.execute(
            select(self.model).options(
                joinedload(self.model.answers).options(
                    joinedload(Answer.difficulty)
                ),
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
                joinedload(self.model.answers).options(
                    joinedload(Answer.difficulty)
                ),
                joinedload(self.model.category),
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
        data: dict[str, Any] = obj_data.model_dump(exclude_none=True)
        data_answer: list[dict[str, str]] = data.pop('answers')
        data_blocks: list[dict[str, Any]] = data.pop('blocks')
        data_category: dict[str, str] = data.pop('category')

        category_in_db = await category_crud.get_category_by_title(
            session, data_category.get('title')
        )

        if not category_in_db:
            data['category'] = Category(**data_category)
        else:
            data['category_id'] = category_in_db.id

        new_question = self.model(**data)

        # Добавление ответов к вопросу
        for answer in data_answer:
            difficulty = answer.pop('difficulty', None)
            if difficulty is None:
                difficulty = 'Сложность отсутствует'
            difficulty_in_db = await difficulty_crud.get_by_title(
                session, title=difficulty
            )

            if not difficulty_in_db:
                answer['difficulty'] = Difficulty(title=difficulty)
            else:
                answer['difficulty_id'] = difficulty_in_db.id

            new_question.answers.append(Answer(**answer))

        # Добавление блоков к вопросу
        for block in data_blocks:
            block_for_assoc = await block_crud.get_by_title(
                session, block.get('title')
            )
            if not block_for_assoc:
                block_for_assoc = Block(**block)

            new_question.blocks.append(Association(block=block_for_assoc))

        session.add(new_question)
        await session.commit()
        await session.refresh(new_question)
        return new_question

    async def get_question_by_block(
        self, session: AsyncSession, block_id: int
    ) -> list[Question]:

        questions = await session.execute(
            select(self.model)
            .where(
                and_(
                    Association.block_id == block_id,
                    Association.question_id == self.model.id,
                )
            )
            .options(
                joinedload(self.model.answers),
                joinedload(self.model.blocks).options(
                    joinedload(Association.block),
                ),
            )
        )

        return questions.scalars().unique().all()

    async def get_random_question(
        self,
        session: AsyncSession,
        category_id: int | None = None,
        grade: str | None = None,
    ) -> Question:
        query = (
            select(self.model)
            .options(
                joinedload(self.model.answers),
                joinedload(self.model.blocks).options(
                    joinedload(Association.block),
                ),
            )
            .order_by(func.random())
        )

        if category_id is not None:
            query = query.where(self.model.category_id == category_id)
        grade_id = await difficulty_crud.get_by_title(session, title=grade)
        if grade is not None:
            query = query.where(
                and_(
                    Answer.difficulty_id == grade_id.id,
                    Answer.question_id == self.model.id,
                )
            )
        question = await session.execute(query)
        return question.scalar()


question_crud = CRUDQuestion(Question)
