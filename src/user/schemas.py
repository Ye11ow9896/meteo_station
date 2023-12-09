from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class MeteoStationsInUser(BaseModel):
    id: int
    name: str
    lat: float
    lon: float
    has_video_server: bool
    video_server_ip: Optional[str] = None
    video_server_port: Optional[str] = None
    video_server_stream_path: Optional[str] = None
    has_timelapse: bool
    video_server_snapshot_path: Optional[str] = None


class User(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    surname: Optional[str] = None
    login: Optional[str] = None
    create_date: Optional[datetime] = None
    password_hash: Optional[str] = None
    meteo_station: Optional[list[MeteoStationsInUser]] = None


class RequestCreateUser(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    login: str
    password_hash: str = Field(alias='password')


class RequestUpdateUser(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None


class ResponseCreateUpdateUser(BaseModel):
    id: int
    name: Optional[str] = None
    surname: Optional[str] = None
    login: str
    create_date: datetime


class ResponseCurrentUser(ResponseCreateUpdateUser):
    meteo_station: Optional[list[MeteoStationsInUser]] = None
