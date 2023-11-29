from fastapi import APIRouter, status

from src.auth.dependencies import get_auth_service
from src.auth import schemas

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post(
    path='/login',
    status_code=status.HTTP_201_CREATED,
)
async def login(
        credentials_dto: schemas.LoginCredentials,
        auth_service: get_auth_service()
):
    return await auth_service.login_or_409(credentials_dto=credentials_dto)


@auth_router.get(
    path="/refresh",
    status_code=status.HTTP_200_OK
)
async def read_items(
        auth_service: get_auth_service(),
):
    return auth_service.refresh()


@auth_router.delete(
    path='/logout',
    status_code=status.HTTP_200_OK,
    description='Protected endpoint.'
)
async def logout(
        auth_service: get_auth_service(),
):
    await auth_service.check_access_to_endpoint()
    return auth_service.logout()
