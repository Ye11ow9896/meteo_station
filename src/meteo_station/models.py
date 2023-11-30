from typing import Optional, Annotated, Any

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.base.models import Base
from src.meteo_station import schemas
from src.user.models import User

str50 = Annotated[str, 50]
str255 = Annotated[str, 255]
ip_str = Annotated[str, 15]
port_str = Annotated[str, 5]


class MeteoStation(Base):
    __tablename__ = 'meteo_station'
    __repr_fields__ = (
        'id',
        'id_user',
        'name',
        'lat',
        'lon',
        'has_video_server',
        'video_server_ip',
        'video_server_port',
        'video_server_stream_path',
        'has_timelapse',
        'video_server_snapshot_path',
        'os_login',
        'os_password_hash',
    )

    def __init__(self, **kw: Any):
        super().__init__(**kw)

    id_user: Mapped = mapped_column(ForeignKey('users.id'), nullable=False)
    name: Mapped[Optional[str50]] = mapped_column(unique=True, nullable=False)
    lat: Mapped[float] = mapped_column(nullable=False)
    lon: Mapped[float] = mapped_column(nullable=False)
    has_video_server: Mapped[bool] = mapped_column(nullable=False, default=True)
    video_server_ip: Mapped[ip_str]
    video_server_port: Mapped[port_str]
    video_server_stream_path: Mapped[str]
    has_timelapse: Mapped[bool] = mapped_column(nullable=False, default=True)
    video_server_snapshot_path: Mapped[str]
    os_login: Mapped[str50]
    os_password_hash: Mapped[str50]

    user: Mapped["User"] = relationship(back_populates="meteo_station")

    def get_table_fields(self) -> schemas.MeteoStation:
        return schemas.MeteoStation(
            id=self.id,
            id_user=self.id_user,
            name=self.name,
            lat=self.lat,
            lon=self.lon,
            has_video_server=self.has_video_server,
            video_server_ip=self.video_server_ip,
            video_server_port=self.video_server_port,
            video_server_stream_path=self.video_server_stream_path,
            has_timelapse=self.has_timelapse,
            video_server_snapshot_path=self.video_server_snapshot_path,
            os_login=self.os_login,
            os_password_hash=self.os_password_hash,
        )
