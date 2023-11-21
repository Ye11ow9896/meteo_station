from typing import Optional

from src.base.uow import SqlAlchemyUnitOfWork
from src.base.exceptions import NotFoundException
from src.user.exceptions import LoginAlreadyExist
from src.user import schemas


class UserService:
    @staticmethod
    async def create_user(user_dto: schemas.RequestCreateUpdateUser) -> schemas.User:
        async with SqlAlchemyUnitOfWork() as uow:
            if await uow.user.get_by_login_or_none(login=user_dto.login):
                raise LoginAlreadyExist()
            new_user = await uow.user.create(data=user_dto.model_dump())
            await uow.commit()
        return new_user

    @staticmethod
    async def get_or_404(id: int) -> Optional[schemas.User]:
        async with SqlAlchemyUnitOfWork() as uow:
            user = await uow.user.read(id=id)
            uow.commit()
        if not user:
            raise NotFoundException(detail=f'User not found by id {id}')
        return user

    @staticmethod
    async def get_list() -> list[schemas.ResponseCreateUpdateUser]:
        async with SqlAlchemyUnitOfWork() as uow:
            return await uow.user.list()

