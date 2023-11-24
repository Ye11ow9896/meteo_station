import hashlib
from typing import Optional

from config import SALT
from src.base.uow import SqlAlchemyUnitOfWork
from src.base.exceptions import NotFoundException
from src.user.exceptions import BadUserPasswordException, BadUserLoginExceptions
from src.user import schemas


class BadUserPasswordException:
    pass


class UserService:

    async def create_user(self, user_dto: schemas.RequestCreateUpdateUser) -> schemas.User:
        """Method get user's data and create new user in database"""

        new_user = schemas.ResponseCreateUpdateUser(
            name=user_dto.name,
            surname=user_dto.surname,
            login=user_dto.login,
            password_hash=self.__hashing_password(password=user_dto.password_hash)
        )
        async with SqlAlchemyUnitOfWork() as uow:
            if await uow.user.get_by_login_or_none(login=user_dto.login):
                raise BadUserLoginExceptions()
            created_user = await uow.user.create(data=new_user)
            await uow.commit()
        return created_user

    @staticmethod
    async def get_or_404(id: int) -> Optional[schemas.User]:
        """Method get user's id and return user or raise 404 error"""

        async with SqlAlchemyUnitOfWork() as uow:
            user = await uow.user.read(id=id)
            uow.commit()
        if not user:
            raise NotFoundException(detail=f'User with id {id} not found.')
        return user

    @staticmethod
    async def get_list() -> list[schemas.ResponseCreateUpdateUser]:
        """Method return list of all users"""

        async with SqlAlchemyUnitOfWork() as uow:
            return await uow.user.list()

    async def login_or_409(self, user_credentials: schemas.UserCredentials) -> schemas.ResponseCreateUpdateUser:
        """Method login user or raise 409 error"""

        async with SqlAlchemyUnitOfWork() as uow:
            user = await uow.user.get_by_login_or_none(login=user_credentials.login)
        if not user:
            raise BadUserLoginExceptions()
        if self.__hashing_password(password=user_credentials.password) != user.password_hash:
            raise BadUserPasswordException()
        return user

    @staticmethod
    async def __hashing_password(password: str) -> str:
        """Method get user's password and return hashed password with salt"""

        convert_password = str.encode(password + str(SALT), encoding='utf-8')
        return hashlib.md5(convert_password).hexdigest()
