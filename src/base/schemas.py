from enum import StrEnum
from fastapi import Query
from typing import Optional

from pydantic import BaseModel, Field


class Direction(StrEnum):
    asc: str = 'asc'
    desc: str = 'desc'


class Pagination(BaseModel):
    limit: Optional[int] = Field(Query(default=1000))
    offset: Optional[int] = Field(Query(default=0))
    sortBy: Optional[str] = Field(Query(default='id'))
    direction: Direction = Field(Query(default='asc'))
