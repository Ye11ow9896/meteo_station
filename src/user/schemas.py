from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class User(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    surname: Optional[str] = None
    login: Optional[str] = None
    create_date: Optional[datetime] = None
    password_hash: Optional[str] = None


class RequestCreateUpdateUser(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    login: str
    password_hash: str = Field(alias='password')


class ResponseCreateUpdateUser(BaseModel):
    id: int
    name: Optional[str] = None
    surname: Optional[str] = None
    login: str
    create_date: datetime


class UserCredentials(BaseModel):
    login: str
    password: str
