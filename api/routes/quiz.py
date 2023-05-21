
from fastapi import (
    APIRouter,
    Depends,
    status,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from api.services import (
    create_categories,
    create_quizs,
    request_quiz_questions,
)
from database.base import (
    get_async_db,
)
from database.schema import (
    CategorySchema,
    QuestionResponseSchema,
    QuestionSchema,
    QuestionRequestSchema,
)


router = APIRouter(prefix='/quiz', tags=['Quiz'])


@router.post('', status_code=status.HTTP_201_CREATED)
async def get_questions(
    data: QuestionRequestSchema,
    db: AsyncSession = Depends(get_async_db),
) -> list[QuestionResponseSchema]:
    """Get quiz questions.

    Questions are requested from a third-party service and will be saved in the database.
    If such a question already exists in the database, a new request is sent until a unique question is received.
    """

    questions = await request_quiz_questions(data.questions_num)

    if questions:
        questions = [QuestionSchema.parse_obj(question) for question in questions]
        question_categorys = [CategorySchema.parse_obj(question.category) for question in questions]
        await create_categories(question_categorys, db)
        quizs = await create_quizs(questions, db)
    else:
        quizs = []

    return quizs
