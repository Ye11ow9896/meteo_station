from fastapi import APIRouter, status

from src.auth.dependencies import get_auth_service
from src.base.dependencies import set_pagination_to_query_path
from src.user import schemas
from src.user.dependencies import get_user_service

user_router = APIRouter(prefix='/user', tags=['User'])


@user_router.post(
    path='/create',
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ResponseCreateUpdateUser,
    description='Protected method.'
)
async def create_user(
        user_dto: schemas.RequestCreateUser,
        user_service: get_user_service(),
) -> schemas.ResponseCreateUpdateUser:
    return await user_service.create(user_dto=user_dto)


@user_router.get(
    path='/current/features',
    status_code=status.HTTP_200_OK,
    response_model=schemas.ResponseCurrentUser,
    description='Protected method'
)
async def read_user(user_service: get_user_service(), auth_service: get_auth_service()):
    authorized_user = await auth_service.check_access_or_raise_401()
    return await user_service.get(id=authorized_user.id)


@user_router.get(
    path='/list',
    status_code=status.HTTP_200_OK,
    response_model=list[schemas.ResponseCreateUpdateUser],
    description='Protected method.'
)
async def get_user_list(
        user_service: get_user_service(),
        auth_service: get_auth_service(),
        pagination: set_pagination_to_query_path(),
) -> list[schemas.ResponseCreateUpdateUser]:
    await auth_service.check_access_or_raise_401()
    return await user_service.get_list(pagination=pagination)
