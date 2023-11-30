from datetime import datetime
from typing import Optional, Annotated, Any, List

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.base.models import Base
from src.user import schemas
from src.meteo_station.models import MeteoStation

str50 = Annotated[str, 50]


class User(Base):
    __tablename__ = 'user'
    __repr_fields__ = ('id', 'name', 'surname', 'login', 'create_date', 'password_hash')

    def __init__(self, **kw: Any):
        super().__init__(**kw)

    name: Mapped[Optional[str50]]
    surname: Mapped[Optional[str50]]
    login: Mapped[str50] = mapped_column(unique=True, nullable=False)
    create_date: Mapped[datetime] = mapped_column(nullable=False, server_default=func.now())
    password_hash: Mapped[str50] = mapped_column(nullable=False)

    meteo_station: Mapped[List["MeteoStation"]] = relationship(back_populates="user")

    def get_table_fields(self) -> schemas.User:
        return schemas.User(
            id=self.id,
            name=self.name,
            surname=self.surname,
            login=self.login,
            create_date=self.create_date,
            password_hash=self.password_hash,
        )
