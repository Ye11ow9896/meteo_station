from starlette.responses import JSONResponse

from src.auth import schemas
from src.auth.exceptions import BadLoginExceptions, BadPasswordException
from src.auth.jwt import JWT
from src.base.uow import SqlAlchemyUnitOfWork
from src.base.utils import UtilsService


class AuthService(UtilsService):

    async def login_or_409(self, credentials_dto: schemas.LoginCredentials):
        """Method login user or raise 409 error"""

        async with SqlAlchemyUnitOfWork() as uow:
            user = await uow.user.get_by_login_or_none(login=credentials_dto.login)
        if user is None:
            raise BadLoginExceptions
        if not self._is_verified_password(password=credentials_dto.password, password_hash=user.password_hash):
            raise BadPasswordException
        tok = self.set_access_cookie(login=user.login)
        return tok

    def set_access_cookie(self, login: str) -> str:
        access_token = JWT.set_access_cookie(login=login)
        response = JSONResponse(content={'message': 'Create a new cookie!'})
        response.set_cookie(key="fakesession", value=access_token)
        return response

    def set_refresh_cookie(self, refresh_cookie: str) -> str:
        ...

    @staticmethod
    def create_access_token(login: str) -> str:
        return JWT.create_access_token(login=login)

    @staticmethod
    def create_refresh_token(self, login: str) -> str:
        return JWT.create_refresh_token(login=login)
