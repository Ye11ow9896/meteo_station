from fastapi import APIRouter, status

from src.user import schemas
from src.user.dependencies import get_user_service

user_router = APIRouter(
    prefix='/user',
    tags=['User']
)


@user_router.post(
    path='/create',
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ResponseCreateUpdateUser
)
async def create_user(
        user_dto: schemas.RequestCreateUpdateUser,
        user_service: get_user_service(),
) -> schemas.ResponseCreateUpdateUser:
    return await user_service.create_user(user_dto=user_dto)


@user_router.get(
    path='/list',
    status_code=status.HTTP_200_OK,
    response_model=list[schemas.ResponseCreateUpdateUser]
)
async def get_user_list(
        user_service: get_user_service(),
) -> list[schemas.ResponseCreateUpdateUser]:
    return await user_service.get_list()
