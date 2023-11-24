from typing import Annotated

from fastapi import Depends

from src.auth.service import AuthService


def get_auth_service():
    """ Dependency injection for auth service """
    return Annotated[AuthService, Depends(AuthService)]
