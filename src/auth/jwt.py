from datetime import timedelta, datetime
from enum import Enum

from jose import jwt

from fastapi import Response
from config import TOKEN_SECRET_KEY, JWT_CRYPT_ALGORITHM, REFRESH_TOKEN_EXPIRE, ACCESS_TOKEN_EXPIRE


class TokenTypes(str, Enum):
    ACCESS_TOKEN = 'access'
    REFRESH_TOKEN = 'refresh'


class JWT:
    """JWT class."""

    @classmethod
    def set_access_cookie(cls, login):
        token = cls.create_access_token(login=login)
        response = Response()
        response.set_cookie(
            'access_token_cookie',
            token,
            max_age=None,
            path='/',
            domain=None,
            secure=False,
            httponly=True,
            samesite=None
        )
        return token

    @classmethod
    def create_access_token(cls, login: str) -> str:
        """Method create access token and return it"""

        return cls._create_token(token_type=TokenTypes.ACCESS_TOKEN, expires_delta=ACCESS_TOKEN_EXPIRE, login=login)

    @classmethod
    def create_refresh_token(cls, login: str) -> str:
        """Method create refresh token and return it"""

        return cls._create_token(token_type=TokenTypes.REFRESH_TOKEN, expires_delta=REFRESH_TOKEN_EXPIRE, login=login)

    @classmethod
    def _create_token(cls, token_type: TokenTypes, expires_delta: timedelta, login: str) -> str:
        """Method for creating tokens"""

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
    def decode(token: str) -> dict:
        """Decode token."""

        return jwt.decode(token, TOKEN_SECRET_KEY, JWT_CRYPT_ALGORITHM)
