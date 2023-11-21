from abc import ABC, abstractmethod
from typing import Annotated

from src.base.repository import AbstractRepository
from src.database import async_session
from src.user.repository import UserRepository


class AbstractUnitOfWork(ABC):
    user: AbstractRepository

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, exc_tb):
        await self.rollback()

    @abstractmethod
    async def commit(self):
        raise NotImplementedError()

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError()


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    user: UserRepository

    def __init__(self, session_factory=async_session):
        super().__init__()
        self.__session_factory = session_factory

    async def __aenter__(self):
        self.__session = self.__session_factory()
        self.user: UserRepository = UserRepository(self.__session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await super().__aexit__(exc_type, exc_val, exc_tb)
        await self.__session.close()

    async def commit(self):
        await self.__session.commit()

    async def rollback(self):
        await self.__session.rollback()
