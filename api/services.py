import logging
from typing import (
    Any,
)

from fastapi import (
    HTTPException,
    status,
)
from httpx import (
    AsyncClient,
)
from sqlalchemy.ext.asyncio.session import (
    AsyncSession,
)

from config import (
    config,
)
from database.category_repository import (
    CategoryRepository,
)
from database.models import (
    Quiz,
)
from database.quiz_repository import (
    QuizRepository,
)
from database.schema import (
    CategorySchema,
    QuestionSchema,
)


ONE = 1


async def request_quiz_questions(count: int) -> list[dict[str, Any]]:
    """Request to a third-party service to receive questions for the quiz."""

    questions = []
    url = config.QUIZ_URL.format(count=count)

    async with AsyncClient() as async_client:
        response = await async_client.get(url=url)

        if response.status_code == status.HTTP_200_OK:
            questions = response.json()
        else:
            raise HTTPException(
                status_code=status.HTTP_204_NO_CONTENT,
                detail=(
                    f'The quiz questions were not received. '
                    f'The quiz server returned the status {response.status_code}'
                )
            )

    return questions


async def create_categories(question_categorys: list[CategorySchema], db: AsyncSession) -> None:
    """Creating quiz categories."""

    category_repository = CategoryRepository(db)

    for category in question_categorys:
        await category_repository.add_ignore_exist(category)


async def create_quizs(questions: list[QuestionSchema], db: AsyncSession) -> list[Quiz]:
    """Creating quizzes."""

    quiz_repository = QuizRepository(db)
    category_repository = CategoryRepository(db)
    quizs = []

    for question in questions:
        question, is_new = await get_qnique_question(db, question)

        if is_new:
            category = CategorySchema.parse_obj(question.category)
            await category_repository.add_ignore_exist(category)

        quizs.append(
            Quiz(
                id=question.id,
                answer=question.answer,
                question=question.question,
                value=question.value,
                airdate=question.airdate,
                category_id=question.category_id,
                game_id=question.game_id,
            )
        )

    return await quiz_repository.add_all(quizs)


async def get_qnique_question(
    db: AsyncSession,
    question: QuestionSchema,
    limit_requests: int = 100,
) -> tuple[QuestionSchema, bool]:
    """Getting a unique quiz question.

    If a quiz question is found in the database, a request is sent to get a new question until
    a unique one is received, or the request limit runs out.
    """

    quiz_repository = QuizRepository(db)
    exist_question = await quiz_repository.get_by_id(question.id)
    is_new = False

    if exist_question:
        for _ in range(limit_requests):
            new_question, *_ = await request_quiz_questions(ONE)
            new_question = QuestionSchema.parse_obj(new_question)
            exist_question = await quiz_repository.get_by_id(new_question.id)

            if not exist_question:
                question = new_question
                is_new = True
                break
        else:
            logging.info(f'No unique quiz question found, limit_requests={limit_requests}')
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='No unique quiz question found.',
            )

    return question, is_new
