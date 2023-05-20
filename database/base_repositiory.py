
from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    Generic,
    TypeVar,
)


T = TypeVar('T')


class BaseRepository(ABC, Generic[T]):
    """Base class for repositories."""

    @abstractmethod
    async def add(self, obj: T) -> None:
        """Add new object to repository."""

    @abstractmethod
    async def update(self, obj: T) -> None:
        """Update existing object in the repository."""

    @abstractmethod
    async def delete(self, obj_id: T) -> None:
        """Delete an existing object from a repository."""

    @abstractmethod
    def get_by_id(self, obj_id: int) -> T | None:
        """Retrieve an object by its id."""
