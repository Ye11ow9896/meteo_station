from src.base.models import Base
from src.base.utils import UtilsService

from src.meteo_station import schemas


class MeteoStationService(Base, UtilsService):

    async def create(self, user_id: int, station_dto: schemas.RequestCreateMeteoStation):
        station_dto.__setattr__('user_id', user_id)
        station_dto.os_password_hash = self._get_hashed_password(station_dto.os_password_hash)
