import logging

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.answer import answer_crud
from app.crud.block import block_crud
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
    bt: str = None,
    session: AsyncSession = Depends(get_async_session),
):
    all_blocks = await block_crud.get_multi(session)
    context = {
        'request': request,
        'blocks': all_blocks,
    }
    if bt is not None:
        questions = await block_crud.get_multy_by_title(session, bt)
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


@router.post('/asso_q', response_model=QuestionCreate)
async def asso(
    data: QuestionCreate, session: AsyncSession = Depends(get_async_session)
) -> QuestionDB:
    l_block = []
    l_answer = []
    all_obj = []
    # for block in data.blocks:
    #     new_block = block_crud.create(session, block)
    #     l_block.append(block)
    new_q = await question_crud.create(session, data)

    # for answer in data.answers:
    #     new_answer = answer_crud.create(session, answer)
    #     l_answer.append(new_answer)
    # for _ in range(max(len(l_block), len(l_answer))):
    #     obj = Association()
    #     all_obj

    # session.add_all(all_obj)
    await session.commit()
    # for i in all_obj:
    await session.refresh(new_q)
    return new_q


@router.get('/test_111')
async def assoc_test(
    session: AsyncSession = Depends(get_async_session),
) -> QuestionDB:
    data = {
        "title": "strin_fow_assoc",
        "additional": "string_fow_assoc",
        "text_question": "string_fow_assoc",
        "answers": [
            {"content": "string_fow_assoc", "difficulty": "string_fow_assoc"},
            {"content": "string_fow_assoc2", "difficulty": "string_fow_assoc"},
            {"content": "string_fow_assoc3", "difficulty": "string_fow_assoc"},
        ],
        "blocks": [
            {"title": "string_fow_assoc", "level": 1},
            {"title": "string_fow_assoc2", "level": 2},
            {"title": "string_fow_assoc3", "level": 3},
        ],
        "time_decision": 1,
    }

    data_answer = data.pop('answers')
    data_blocks = data.pop('blocks')

    new_question = Question(**data)
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
    return await question_crud.get_by_id_v2(session, new_question.id)
