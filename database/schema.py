from datetime import (
    datetime,
)

from pydantic import (
    BaseModel,
    PositiveInt,
)


class QuestionRequestSchema(BaseModel):
    questions_num: PositiveInt


class CategorySchema(BaseModel):

    id: int
    title: str
    created_at: datetime
    updated_at: datetime
    clues_count: int | None

    class Config:
        orm_mode = True


class QuestionSchema(BaseModel):

    id: int
    answer: str
    question: str
    value: int | None
    airdate: datetime
    category_id: int
    game_id: int
    created_at: datetime
    updated_at: datetime
    category: CategorySchema

    class Config:
        orm_mode = True


class QuestionResponseSchema(BaseModel):
    question: str

    class Config:
        orm_mode = True
