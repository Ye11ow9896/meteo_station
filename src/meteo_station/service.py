from src.base.exceptions import AlreadyExistsException, NotFoundException
from src.base.uow import SqlAlchemyUnitOfWork
from src.base.utils import UtilsService

from src.meteo_station import schemas


class MeteoStationService(UtilsService):

    async def create_or_409(self, user_id: int, station_dto: schemas.RequestCreateMeteoStation):
        """Method is creating new meteo-station by current user id. If name already exists it raise 409."""

        station_dto.user_id = user_id
        station_dto.os_password_hash = self._get_hashed_password(station_dto.os_password_hash)

        async with SqlAlchemyUnitOfWork() as uow:
            if await uow.meteo_station.get_by_name_or_none(name=station_dto.name):
                raise AlreadyExistsException(detail=f'Meteo station with name {station_dto.name} already exists!')
            station = await uow.meteo_station.create(data=station_dto.model_dump())
        return station

    @staticmethod
    async def get_by_id_or_404(id: int) -> schemas.ResponseGetMeteoStation:
        """Method returns meteo-station by id or raise 404."""

        async with SqlAlchemyUnitOfWork() as uow:
            station = await uow.meteo_station.read_or_none(id=id)
            if not station:
                raise NotFoundException(detail=f'Meteo station with id {id} not found!')
        return station
