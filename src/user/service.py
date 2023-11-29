from typing import Optional

from src.base.schemas import Pagination
from src.base.uow import SqlAlchemyUnitOfWork
from src.base.exceptions import NotFoundException, AlreadyExistsException
from src.base.utils import UtilsService
from src.user import schemas


class UserService(UtilsService):
    """User service class"""

    async def create_user(self, user_dto: schemas.RequestCreateUpdateUser) -> schemas.User:
        """Method get user's data and create new user in database or raise 409 exception"""

        user_dto.password_hash = self._hashing_password(password=user_dto.password_hash)
        async with SqlAlchemyUnitOfWork() as uow:
            if await uow.user.get_by_login_or_none(login=user_dto.login):
                raise AlreadyExistsException(detail=f'User with login {user_dto.login} already exists!')
            created_user = await uow.user.create(data=user_dto.model_dump())
            await uow.commit()
        return created_user

    @staticmethod
    async def get_or_404(id: int) -> Optional[schemas.User]:
        """Method get user's id and return user or raise 404 error"""

        async with SqlAlchemyUnitOfWork() as uow:
            user = await uow.user.read(id=id)
            uow.commit()
        if not user:
            raise NotFoundException(detail=f'User with id {id} not found!')
        return user

    @staticmethod
    async def get_list(pagination: Pagination) -> list[schemas.ResponseCreateUpdateUser]:
        """Method return list of all users"""

        async with SqlAlchemyUnitOfWork() as uow:
            return await uow.user.list(pagination=pagination)


