from abc import abstractmethod, ABC

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """
    MainBase class for creating all models.
    """

    __abstract__ = True
    __repr_fields__: tuple[str, ...] = ('id',)

    id: Mapped[int] = mapped_column(primary_key=True)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        attrs = ', '.join(
            f'{field}: {getattr(self, field)}'
            for field in self.__repr_fields__
        )
        return f'{self.__class__.__name__}({attrs})'


class AbstractBase(ABC):
    @abstractmethod
    def get_table_fields(self):
        raise NotImplemented
