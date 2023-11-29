from copy import copy
from datetime import timedelta, datetime
from enum import StrEnum
from typing import Annotated, Optional

from jose import jwt

from fastapi import Response
from starlette.requests import Request

from config import TOKEN_SECRET_KEY, JWT_CRYPT_ALGORITHM, REFRESH_TOKEN_EXPIRE, ACCESS_TOKEN_EXPIRE
from src.auth.exceptions import UnauthorizedException, TokenExpiredException
from src.auth import schemas


class TokenTypes(StrEnum):
    ACCESS_TOKEN = 'access_token'
    REFRESH_TOKEN = 'refresh_token'


class AuthJWT:
    """AuthJWT class."""

    def __init__(
            self,
            response: Annotated[Response, Response()],
            request: Request
    ):
        self.__response = response
        self.__request = request
        self.__access_token = request.cookies.get(TokenTypes.ACCESS_TOKEN)
        self.__refresh_token = request.cookies.get(TokenTypes.REFRESH_TOKEN)

    def _delete_cookies(self):
        """Method is deleting cookies."""

        return {
            self.__response.delete_cookie(key=TokenTypes.ACCESS_TOKEN),
            self.__response.delete_cookie(key=TokenTypes.REFRESH_TOKEN)
        }

    def _get_login_from_access_token_or_401(self) -> str:
        """Method is taking login from refresh token or raise 401."""

        if self.__access_token is None:
            raise UnauthorizedException
        return self.__get_token_payload_or_401(token=self.__access_token, expire_delta=REFRESH_TOKEN_EXPIRE)['login']

    def _get_login_from_refresh_token_or_401(self):
        """Method is taking login from refresh token or raise 401."""

        if self.__refresh_token is None:
            raise UnauthorizedException
        return self.__get_token_payload_or_401(token=self.__refresh_token, expire_delta=REFRESH_TOKEN_EXPIRE)['login']

    def _set_access_cookie(self, login: str) -> Response:
        """Method is setting access token and wrapped it for cookie and send it to cookie storage."""

        access_token = self.__create_token(
            token_type=TokenTypes.ACCESS_TOKEN,
            expires_delta=ACCESS_TOKEN_EXPIRE,
            login=login
        )
        return self.__set_cookie(token=access_token, key=TokenTypes.ACCESS_TOKEN, response=self.__response)

    def _set_refresh_cookie(self, login) -> Response:
        """Method is setting refresh token and wrapped it for cookie and send it to cookie storage."""

        refresh_token = self.__create_token(
            token_type=TokenTypes.REFRESH_TOKEN,
            expires_delta=REFRESH_TOKEN_EXPIRE,
            login=login,
        )
        return self.__set_cookie(token=refresh_token, key=TokenTypes.REFRESH_TOKEN, response=self.__response)

    def __get_token_payload_or_401(self, token: str, expire_delta: timedelta) -> dict:
        """Method takes token payload or raise 401 if token has expired"""

        payload = self.__decode(token=token)
        if not self.__is_token_expired(payload=payload, expire_delta=expire_delta):
            return payload

    @staticmethod
    def __is_token_expired(payload: dict, expire_delta: timedelta) -> Optional[bool]:
        """Method returns False if token has not expired and raise 401 if token has expired"""

        token_expire = datetime.fromisoformat(payload.get('expire')) + expire_delta
        if token_expire <= datetime.utcnow():
            raise TokenExpiredException
        return False

    @classmethod
    def __set_cookie(cls, token, key: TokenTypes, response: Response) -> Response:
        """Method is setting cookie to local storage."""

        response.status_code = 200
        response.set_cookie(key, token)
        return response

    @classmethod
    def __create_token(cls, token_type: TokenTypes, expires_delta: timedelta, login: str) -> str:
        """Method for creating tokens."""

        expire = datetime.utcnow() + expires_delta
        payload = {
            "login": login,
            "expire": expire.isoformat(),
            "type": token_type,
        }
        return cls.__encode(payload=payload)

    @staticmethod
    def __encode(payload: dict) -> str:
        """Encode payload."""

        return jwt.encode(payload, TOKEN_SECRET_KEY, JWT_CRYPT_ALGORITHM)

    @staticmethod
    def __decode(token: str) -> dict:
        """Decode token."""

        return jwt.decode(token, TOKEN_SECRET_KEY, JWT_CRYPT_ALGORITHM)
