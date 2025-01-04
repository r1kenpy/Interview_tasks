import logging
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from app.core.db import get_async_session
from app.schemas.question import QuestionCreate, QuestionDB
from app.schemas.answer import AnswerCreate, AnswerDB
from app.schemas.block import BlockDB, BlockCreate
from app.crud.question import question_crud
from app.crud.answer import answer_crud
from app.crud.block import block_crud
from app.models.answer import Answer

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
    request: Request, session: AsyncSession = Depends(get_async_session)
):
    blocks = await block_crud.get_multi(session)
    context = {
        'request': request,
        'blocks': blocks,
    }
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
