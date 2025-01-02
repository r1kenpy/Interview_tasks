from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.schemas.question import QuestionCreate, QuestionDB
from app.schemas.answer import AnswerCreate, AnswerDB
from app.schemas.block import BlockDB, BlockCreate
from app.crud.question import question_crud
from app.crud.answer import answer_crud


router = APIRouter()


@router.post(
    '/question', response_model=QuestionDB, response_model_exclude=True
)
async def create_Q(
    data: QuestionCreate,
    session: AsyncSession = Depends(get_async_session),
):
    new_db = await question_crud.create(session, data)
    await session.commit()
    await session.refresh(new_db)
    return new_db


@router.post(
    '/answer', response_model=AnswerDB, response_model_exclude_none=True
)
async def create_A(
    data: AnswerCreate,
    session: AsyncSession = Depends(get_async_session),
):
    new_db = await answer_crud.create(session, data)
    await session.commit()
    await session.refresh(new_db)
    return new_db


@router.post(
    '/block', response_model=BlockDB, response_model_exclude_none=True
)
async def create_B(
    data: BlockCreate,
    session: AsyncSession = Depends(get_async_session),
):
    new_db = await answer_crud.create(session, data)
    await session.commit()
    await session.refresh(new_db)
    return new_db
