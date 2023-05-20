
from sqlalchemy import (
    select,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from database.base_repositiory import (
    BaseRepository,
)
from database.models import (
    Quiz,
)


class QuizRepository(BaseRepository[Quiz]):

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def add(self, obj: Quiz) -> None:
        self.db.add(obj)
        await self.db.flush()

    async def update(self, obj: Quiz) -> None:
        await self.db.merge(obj)

    async def delete(self, obj_id: int) -> None:
        quiz: Quiz | None = await self.db.get(Quiz, obj_id)

        if quiz:
            await self.db.delete(quiz)

    async def get_by_id(self, obj_id: int) -> Quiz | None:
        return await self.db.get(Quiz, obj_id)

    async def add_all(self, objs: list[Quiz]) -> list[Quiz]:
        self.db.add_all(objs)
        await self.db.flush()

        return objs

    async def get_by_id_in(self, ids: list[int]):
        query = select(Quiz.id).where(Quiz.id.in_(ids))

        return (await self.db.execute(query)).scalars().all()
