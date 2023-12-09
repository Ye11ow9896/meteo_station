from abc import ABC, abstractmethod

from sqlalchemy.exc import SQLAlchemyError

from src.database import async_session
from src.user.repository import UserRepository
from src.meteo_station.repository import MeteoStationRepository


class AbstractUnitOfWork(ABC):

    def __init__(self, session_factory=async_session):
        self._session = session_factory()
        self._transaction = None

    async def __aenter__(self):
        await self._create_transaction()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if self._transaction:
            if exc_type:
                await self.rollback()
            else:
                await self.commit()

        await self._close_transaction()

    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def _create_transaction(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def _close_transaction(self) -> None:
        raise NotImplementedError


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    user: UserRepository
    meteo_station: MeteoStationRepository

    async def commit(self):
        try:
            await self._session.commit()
        except SQLAlchemyError as e:
            raise e

    async def rollback(self):
        try:
            await self._session.rollback()
        except SQLAlchemyError as e:
            raise e

    async def _create_transaction(self) -> None:
        if not self._session.in_transaction():
            self._transaction = self._session.begin()
            self.user: UserRepository = UserRepository(self._session)
            self.meteo_station: MeteoStationRepository = MeteoStationRepository(self._session)

    async def _close_transaction(self) -> None:
        await self._session.close()
