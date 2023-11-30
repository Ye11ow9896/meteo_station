from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from src.meteo_station.schemas import MeteoStation


class User(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    surname: Optional[str] = None
    login: Optional[str] = None
    create_date: Optional[datetime] = None
    password_hash: Optional[str] = None
    meteo_station: Optional[list[MeteoStation]] = None


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
    meteo_station: Optional[list[MeteoStation]] = None
