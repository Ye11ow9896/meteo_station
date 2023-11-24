from src.auth import schemas
from src.base.uow import SqlAlchemyUnitOfWork


class AuthService:
    async def authenticate_user(self, login: str, password: str) -> schemas.ResponseLogin:
        """ Method for user authentication """
        async with SqlAlchemyUnitOfWork() as uow:
            user = uow.user.get_by_login_or_none(login=login)

