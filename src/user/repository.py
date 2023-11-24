from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exists
from src.base.repository import SqlRepository
from src.user import schemas
from src.user.models import User


class UserRepository(SqlRepository[User]):
    def __init__(self, a_session: AsyncSession):
        super().__init__(a_session, User)
        self._session = a_session

    async def get_by_login_or_none(self, login) -> Optional[schemas.User]:
        result = await self._session.scalar(
            exists().
            where(User.login == login).
            select()
        )
        return result.get_table_fields() if result else None
