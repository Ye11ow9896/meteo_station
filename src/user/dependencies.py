from typing import Annotated

from fastapi import Depends

from src.user.service import UserService


def get_user_service():
    """ Dependency injection for user service """
    return Annotated[UserService, Depends(UserService)]
