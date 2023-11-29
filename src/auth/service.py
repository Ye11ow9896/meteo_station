from starlette.responses import Response

from src.auth import schemas
from src.auth.exceptions import BadLoginExceptions, BadPasswordException
from src.auth.jwt import AuthJWT
from src.base.exceptions import NotFoundException
from src.base.uow import SqlAlchemyUnitOfWork
from src.base.utils import UtilsService
from src.user import schemas as user_schemas


class AuthService(UtilsService, AuthJWT):

    async def check_access_or_raise_401(self) -> user_schemas.User:
        """
        The method protects access to the endpoint. It checks whether there is access to it.
        Raise 401 or return user
        """

        login = self._get_login_from_access_token_or_401()
        async with SqlAlchemyUnitOfWork() as uow:
            user = await uow.user.get_by_login_or_none(login=login)
        if not user:
            raise NotFoundException(detail=f'User with login {login} not found!')
        return user

    async def login_or_409(self, credentials_dto: schemas.LoginCredentials) -> set[Response]:
        """Method login user or raise 409 error"""

        async with SqlAlchemyUnitOfWork() as uow:
            user = await uow.user.get_by_login_or_none(login=credentials_dto.login)
        if user is None:
            raise BadLoginExceptions
        if not self._is_verified_password(password=credentials_dto.password, password_hash=user.password_hash):
            raise BadPasswordException

        return {
            self._set_access_cookie(login=user.login),
            self._set_refresh_cookie(login=user.login)
        }

    def refresh(self) -> Response:
        """Method is refreshing access token and wrapped it to cookie if refresh token is not expired"""

        login = self._get_login_from_refresh_token_or_401()
        return self._set_access_cookie(login=login)

    def logout(self):
        """Method is deleting all cookies."""

        self._delete_cookies()
