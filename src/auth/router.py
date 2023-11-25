from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

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
    credentials_dto: schemas.LoginCredentials,
):
    # content = {"message": "Come to the dark side, we have cookies"}
    # response = JSONResponse(content=content)
    # response.set_cookie(key="fakesession", value="fake-cookie-session-value")
    # return response
    return await auth_service.login_or_409(credentials_dto=credentials_dto)
