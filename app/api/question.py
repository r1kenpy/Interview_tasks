import logging
from typing import Optional

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.answer import answer_crud
from app.crud.block import block_crud
from app.crud.category import category_crud
from app.crud.question import question_crud
from app.schemas.question import QuestionCreate, QuestionDB

tamplates = Jinja2Templates('app/templates')

router = APIRouter()


logger = logging.getLogger(__file__)

logger.addHandler(logging.StreamHandler())
logger.level = logging.DEBUG


@router.get('/', response_class=HTMLResponse)
async def index(
    request: Request,
    category_id: Optional[int] = None,
    session: AsyncSession = Depends(get_async_session),
):

    all_categories = await category_crud.get_multi(session)
    context = {
        'request': request,
        'categories': all_categories,
    }

    if category_id is not None:
        questions = await question_crud.get_multy_by_category_id(
            session, category_id
        )
    else:
        questions = await question_crud.get_multi_v2(session)

    context['questions'] = questions
    difficulty = set()
    for questions in questions:

        for answer in questions.answers:
            if answer.difficulty is None:
                difficulty.add('Сложность отсутствует')
                continue
            difficulty.add(answer.difficulty)

    context['difficulty'] = sorted(difficulty)
    return tamplates.TemplateResponse('index.html', context)


@router.post('/', response_class=HTMLResponse)
async def index(
    request: Request,
    session: AsyncSession = Depends(get_async_session),
):
    dif = await answer_crud.get_all_difficulty(session)
    context = {
        'request': request,
    }
    return tamplates.TemplateResponse('index.html', context)


@router.get('/answers_dif')
async def answers_dif(session: AsyncSession = Depends(get_async_session)):
    ddd = await answer_crud.get_all_difficulty(session)
    for i in ddd:
        print(i.id)
    return None


@router.get('/block/', response_class=HTMLResponse)
async def block(
    request: Request,
    block_id: Optional[int] = None,
    session: AsyncSession = Depends(get_async_session),
):
    context = {
        'request': request,
        'categories': await category_crud.get_multi(session),
    }
    if block_id is not None:
        context['questions'] = await question_crud.get_question_by_block(
            session, block_id
        )
    # print(block_id)
    # print(context.get('questions'))
    difficulty = set()
    for questions in context.get('questions'):

        for answer in questions.answers:
            if answer.difficulty is None:
                difficulty.add('Сложность отсутствует')
                continue
            difficulty.add(answer.difficulty)

    context['difficulty'] = sorted(difficulty)
    return tamplates.TemplateResponse('index.html', context=context)


@router.post('/create_question')
async def create_question(
    data: QuestionCreate,
    session: AsyncSession = Depends(get_async_session),
) -> QuestionDB:

    new_question = await question_crud.create_v2(session, data)

    return await question_crud.get_by_id_v2(session, new_question.id)
