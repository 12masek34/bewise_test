import logging

from dotenv import (
    load_dotenv,
)
from pydantic import (
    AnyHttpUrl,
    BaseSettings,
)
from pydantic.fields import (
    Field,
)


load_dotenv()
logging.basicConfig(filename='logs.log', level=logging.INFO)


class Config(BaseSettings):

    POSTGRES_DB: str = Field(..., env='ASYNC_POSTGRES_URL')
    POSTGRES_USER: str = Field(..., env='POSTGRES_USER')
    POSTGRES_PASSWORD: str = Field(..., env='POSTGRES_PASSWORD')
    POSTGRES_PORT: int = Field(..., env='POSTGRES_PORT')
    POSTGRES_HOST: str = Field(..., env='POSTGRES_HOST')
    ASYNC_POSTGRES_URL: str = Field(..., env='ASYNC_POSTGRES_URL')

    QUIZ_URL: AnyHttpUrl = 'https://jservice.io/api/random?count={count}'

config = Config()
