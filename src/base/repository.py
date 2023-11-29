from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Type, Optional

from sqlalchemy import select, update, insert, delete, exists, asc, desc
from sqlalchemy.ext.asyncio import AsyncSession

from src.base.exceptions import UnprocessableEntityException
from src.base.schemas import Pagination
from src.base.models import Base

T = TypeVar("T", bound=Base)


class AbstractRepository(Generic[T], ABC):
    @abstractmethod
    async def create(self, record: T) -> T:
        raise NotImplementedError()

    @abstractmethod
    async def read(self, id: int) -> T:
        raise NotImplementedError()

    @abstractmethod
    async def update(self, id: int, data: dict) -> int:
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, id: int) -> int:
        raise NotImplementedError()

    @abstractmethod
    async def list(self, pagination: Pagination) -> list[T]:
        raise NotImplementedError()


class SqlRepository(AbstractRepository[T]):
    def __init__(self, session: AsyncSession, model: Type[T]) -> None:
        self.__session = session
        self.__model = model

    async def create(self, data: dict) -> Type[T]:
        result = await self.__session.scalar(
            insert(self.__model).
            values(**data).
            returning(self.__model)
        )
        return None if result is None else result.get_table_fields()

    async def read(self, id: int) -> Optional[T]:
        return await self.__session.scalar(
            exists().
            where(self.__model.id == id).
            select()
        ) or None

    async def update(self, id: int, data: dict) -> Optional[int]:
        result = await self.__session.scalar(
            exists().
            where(self.__model.id == id).
            update(self.__model).
            values(**data).
            returning(self.__model)
        )
        return None if result is None else result.get_table_fields()

    async def delete(self, id: int) -> int:
        result = await self.__session.scalar(
            exists().
            where(self.__model.id == id).
            delete(self.__model).
            returning(self.__model)
        )
        return None if result is None else result.get_table_fields()

    async def list(self, pagination: Pagination) -> list[Type[T]]:
        sort_direction = asc if pagination.direction == 'asc' else desc

        try:
            field = getattr(self.__model, pagination.sortBy)
        except AttributeError:
            raise UnprocessableEntityException(
                detail=f'Sorting error! The {pagination.sortBy} '
                       f'field does not exist in the {self.__model.__name__} model! '
            )

        result = await self.__session.scalars(
            select(self.__model).
            limit(pagination.limit).
            offset(pagination.offset).
            order_by(sort_direction(field))
        )
        return [row.get_table_fields() for row in result]
