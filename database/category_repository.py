
from sqlalchemy.dialects.postgresql import (
    insert,
)
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)

from database.base_repositiory import (
    BaseRepository,
)
from database.models import (
    Category,
)
from database.schema import (
    CategorySchema,
)


class CategoryRepository(BaseRepository[Category]):

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def add(self, obj: Category) -> None:
        self.db.add(obj)
        await self.db.flush()

    async def update(self, obj: Category) -> None:
        await self.db.merge(obj)

    async def delete(self, obj_id: int) -> None:
        category: Category | None = await self.db.get(Category, obj_id)

        if category:
            await self.db.delete(category)

    async def get_by_id(self, item_id: int) -> Category | None:
        return await self.db.get(Category, item_id)

    async def add_all(self, objs: list[Category]) -> None:
        self.db.add_all(objs)
        await self.db.flush()

    async def add_ignore_exist(self, category: CategorySchema) -> None:
        query = insert(Category).values(**category.dict()).on_conflict_do_nothing()
        await self.db.execute(query)
