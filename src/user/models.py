from datetime import datetime
from typing import Optional, Annotated, Any

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from src.base.models import Base, AbstractBase
from src.user import schemas


str50 = Annotated[str, 50]


class User(Base):
    __tablename__ = 'user'
    __repr_fields__ = ('id', 'username')

    def __init__(self, **kw: Any):
        super().__init__(**kw)

    name: Mapped[Optional[str50]]
    surname: Mapped[Optional[str50]]
    login: Mapped[str50] = mapped_column(unique=True, nullable=False)
    create_date: Mapped[datetime] = mapped_column(nullable=False, server_default=func.now())
    password_hash: Mapped[str50] = mapped_column(nullable=False)

    def get_table_fields(self) -> schemas.User:
        return schemas.User(
            id=self.id,
            name=self.name,
            surname=self.surname,
            create_date=self.create_date,
            login=self.login
        )
