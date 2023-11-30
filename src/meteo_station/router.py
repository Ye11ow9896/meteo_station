from fastapi import APIRouter, status

from src.auth.dependencies import get_auth_service
from src.base.dependencies import set_pagination_to_query_path
from src.meteo_station import schemas
from src.user.dependencies import get_user_service

station_router = APIRouter(prefix='/meteo_station', tags=['Meteo station'])


@station_router.post(
    path='/create',
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ResponseCreateMeteoStation,
    description='Protected method.'
)
async def create_user(
        station_dto: schemas.RequestCreateMeteoStation,
        auth_service: get_auth_service(),
):
    authorized_user = await auth_service.check_access_or_raise_401()
