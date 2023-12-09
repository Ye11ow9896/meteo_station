from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class UserInStation(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    login: Optional[str] = None
    create_date: Optional[datetime] = None


class MeteoStation(BaseModel):
    id: int
    user_id: int
    name: str
    lat: float
    lon: float
    has_video_server: bool
    video_server_ip: Optional[str] = None
    video_server_port: Optional[str] = None
    video_server_stream_path: Optional[str] = None
    has_timelapse: bool
    video_server_snapshot_path: Optional[str] = None
    os_login: Optional[str] = None
    os_password_hash: Optional[str] = None

    user: Optional[UserInStation] = None


class RequestCreateMeteoStation(BaseModel):
    name: str
    lat: float
    lon: float
    has_video_server: bool
    video_server_ip: Optional[str] = None
    video_server_port: Optional[str] = None
    video_server_stream_path: Optional[str] = None
    has_timelapse: bool
    video_server_snapshot_path: Optional[str] = None
    os_login: Optional[str] = None
    os_password_hash: Optional[str] = None

    model_config = ConfigDict(extra='allow')


class ResponseCreateMeteoStation(BaseModel):
    name: str
    lat: float
    lon: float
    has_video_server: bool
    video_server_ip: Optional[str] = None
    video_server_port: Optional[str] = None
    video_server_stream_path: Optional[str] = None
    has_timelapse: bool
    video_server_snapshot_path: Optional[str] = None


class ResponseGetMeteoStation(ResponseCreateMeteoStation):
    user: UserInStation
