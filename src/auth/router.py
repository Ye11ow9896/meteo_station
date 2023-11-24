from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from src.auth.dependencies import get_auth_service
from src.auth import schemas


auth_router = APIRouter(prefix="/api", tags=["auth"])


@auth_router.post(
    path='/login',
    status_code=status.HTTP_200_OK,
    response_model=schemas.ResponseLogin
)
async def login(
    auth_service: get_auth_service(),
    credentials: OAuth2PasswordRequestForm = Depends(),
) -> schemas.ResponseLogin:
    ...


