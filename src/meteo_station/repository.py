from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.base.repository import SqlRepository

from src.meteo_station.models import MeteoStation
from src.meteo_station import schemas


class MeteoStationRepository(SqlRepository[MeteoStation]):
    def __init__(self, a_session: AsyncSession):
        super().__init__(a_session, MeteoStation)
        self._session = a_session

    async def read_or_none(self, id: int) -> schemas.MeteoStation:
        return await self._session.scalar(
            select(MeteoStation).
            where(MeteoStation.id == id).
            options(selectinload(MeteoStation.user))
        )

    async def get_by_name_or_none(self, name: str) -> schemas.MeteoStation:
        result = await self._session.scalar(
            select(MeteoStation).where(MeteoStation.name == name)
        )
        return None if not result else result.get_table_fields()
