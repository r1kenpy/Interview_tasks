import logging
from typing import Optional

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.answer import answer_crud
from app.crud.category import category_crud
from app.crud.question import question_crud
from app.schemas.question import QuestionCreate, QuestionDB

tamplates = Jinja2Templates('app/templates')

router = APIRouter()


logger = logging.getLogger(__file__)

logger.addHandler(logging.StreamHandler())
logger.level = logging.DEBUG


@router.post('/create_question')
async def create_question(
    data: QuestionCreate,
    session: AsyncSession = Depends(get_async_session),
) -> QuestionDB:

    new_question = await question_crud.create_v2(session, data)

    return await question_crud.get_by_id_v2(session, new_question.id)
