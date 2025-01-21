import logging
from pprint import pprint
from typing import Optional

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.answer import answer_crud
from app.crud.block import block_crud
from app.crud.category import category_crud
from app.crud.question import question_crud
from app.models.answer import Answer
from app.models.association import Association
from app.models.block import Block
from app.models.question import Question
from app.schemas.answer import AnswerCreate, AnswerDB
from app.schemas.block import BlockCreate, BlockDB
from app.schemas.question import QuestionCreate, QuestionDB

tamplates = Jinja2Templates('app/templates')

router = APIRouter()


logger = logging.getLogger(__file__)

logger.addHandler(logging.StreamHandler())
logger.level = logging.DEBUG


@router.get('/a_form_link/', response_class=HTMLResponse)
async def a_form(
    request: Request, session: AsyncSession = Depends(get_async_session)
):
    # all = await answer_crud.get_multi_with_question(session)
    all = await question_crud.get_multi_v2(session)
    context = {'request': request, 'all': all}

    return tamplates.TemplateResponse('form.html', context)


@router.get('/', response_class=HTMLResponse)
async def index(
    request: Request,
    category_id: Optional[int] = None,
    session: AsyncSession = Depends(get_async_session),
):

    all_blocks = await block_crud.get_multi(session)
    all_categories = await category_crud.get_multi(session)
    context = {
        'request': request,
        'blocks': all_blocks,
        'categories': all_categories,
    }

    if category_id is not None:
        questions = await question_crud.get_multy_by_category_id(
            session, category_id
        )
        context['questions'] = questions
    else:
        questions = await question_crud.get_multi_v2(session)
        context['questions'] = questions

    return tamplates.TemplateResponse('index.html', context)


@router.get('/all_q', response_model=list[QuestionDB])
async def get_all(session: AsyncSession = Depends(get_async_session)):
    all = await question_crud.get_multi_v2(session)
    return all


@router.post(
    '/question', response_model=QuestionDB, response_model_exclude_none=True
)
async def create_Q(
    data: QuestionCreate,
    session: AsyncSession = Depends(get_async_session),
):
    new_db = await question_crud.create_v2(session, data)
    new_db = await question_crud.get_by_id_with_answer(session, new_db.id)
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


@router.get('/answer', response_model=list[AnswerDB])
async def get_all_answers(session: AsyncSession = Depends(get_async_session)):
    all_ = await answer_crud.get_multi_with_question(session)
    return all_


@router.post(
    '/block', response_model=BlockDB, response_model_exclude_none=True
)
async def create_B(
    data: BlockCreate,
    session: AsyncSession = Depends(get_async_session),
):
    new_db = await block_crud.create(session, data)
    await session.commit()
    await session.refresh(new_db)
    return new_db


@router.post('/create_question')
async def create_question(
    data: QuestionCreate,
    session: AsyncSession = Depends(get_async_session),
) -> QuestionDB:

    new_question = await question_crud.create_v2(session, data)

    return await question_crud.get_by_id_v2(session, new_question.id)
