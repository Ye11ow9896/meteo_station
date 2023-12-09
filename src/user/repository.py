from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.base.repository import SqlRepository
from src.user import schemas
from src.user.models import User


class UserRepository(SqlRepository[User]):
    def __init__(self, a_session: AsyncSession):
        super().__init__(a_session, User)
        self._session = a_session

    async def read_or_none(self, id: int):
        return await self._session.scalar(
            select(User).
            where(User.id == id).
            options(
                selectinload(User.meteo_station)
            )
        )

    async def get_by_login_or_none(self, login) -> Optional[schemas.User]:
        result = await self._session.scalar(
            select(User).where(User.login == login)
        )
        return None if not result else result.get_table_fields()
