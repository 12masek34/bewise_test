import uvicorn
from fastapi import (
    FastAPI,
)

from api.routes import (
    quiz,
)
from database.base import (
    async_init_db,
)


app = FastAPI()
app.include_router(quiz.router)


@app.on_event('startup')
async def startup() -> None:
    await async_init_db()


if __name__ == '__main__':
    uvicorn.run(app=app, host='0.0.0.0', port=8000)
