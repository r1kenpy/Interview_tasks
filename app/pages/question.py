import logging
from typing import Optional

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.category import category_crud
from app.crud.question import question_crud

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
    if block_id is None:
        return RedirectResponse('/')

    if block_id is not None:
        context['questions'] = await question_crud.get_question_by_block(
            session, block_id
        )
    difficulty = set()
    for question in context.get('questions'):

        for answer in question.answers:
            if answer.difficulty is None:
                difficulty.add('Сложность отсутствует')
                continue
            difficulty.add(answer.difficulty)

    context['difficulty'] = sorted(difficulty)
    return tamplates.TemplateResponse('index.html', context=context)


@router.get('/random/', response_class=HTMLResponse)
async def random_question(
    request: Request,
    category_id: int | None = None,
    grade: str | None = None,
    session: AsyncSession = Depends(get_async_session),
):

    question = await question_crud.get_random_question(
        session, category_id, grade
    )
    context = {
        'question': question,
        'request': request,
        'categories': await category_crud.get_multi(session),
    }
    context['selected_category'] = None
    if category_id != 0:
        context['selected_category'] = question.category
    else:
        context['selected_category'] = None

    # Нужно создать таблицу difficulties и забирать уровень сложности,
    #   который присутствует в ответах определенной категории вопроса.
    # context['difficulties'] = await difficulties_crud.get_multi(session, category_id)

    return tamplates.TemplateResponse('random.html', context=context)
