from fastapi import APIRouter, status

from src.auth.dependencies import get_auth_service
from src.meteo_station import schemas
from src.meteo_station.dependencies import get_meteo_station_service

station_router = APIRouter(prefix='/meteo_station', tags=['Meteo station'])


@station_router.post(
    path='/create',
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ResponseCreateMeteoStation,
    description='Protected method.'
)
async def create_meteo_station(
        station_dto: schemas.RequestCreateMeteoStation,
        station_service: get_meteo_station_service(),
        auth_service: get_auth_service(),
):
    authorized_user = await auth_service.check_access_or_raise_401()
    return await station_service.create_or_409(user_id=authorized_user.id, station_dto=station_dto)


@station_router.get(
    path='/get/{id}',
    status_code=status.HTTP_200_OK,
    response_model=schemas.ResponseGetMeteoStation,
    description='Protected method',
)
async def get_meteo_station_by_id(
        id: int,
        station_service: get_meteo_station_service(),
        auth_service: get_auth_service(),
):
    await auth_service.check_access_or_raise_401()
    return await station_service.get_by_id_or_404(id=id)
