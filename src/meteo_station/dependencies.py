from typing import Annotated

from fastapi import Depends

from src.meteo_station.service import MeteoStationService


def get_meteo_station_service():
    """ Dependency injection for user service """
    return Annotated[MeteoStationService, Depends(MeteoStationService)]
