from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exists
from src.base.repository import SqlRepository
from src.user.models import User


class UserRepository(SqlRepository[User]):
    def __init__(self, a_session: AsyncSession):
        super().__init__(a_session, User)
        self._session = a_session

    async def get_by_login_or_none(self, login) -> Optional[str]:
        return await self._session.scalar(
            exists().
            where(User.login == login).
            select()
        ) or None

    async def get_hash_password_by_id(self, id: int) -> Optional[str]:
        stmt = select(User.password_hash).where(User.id == id)
        res = await self._session.execute(stmt)
        return res.scalar()
