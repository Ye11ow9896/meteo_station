from typing import Optional

from pydantic import BaseModel, Field


class Pagination(BaseModel):
    limit: Optional[int] = Field(default=None)
    offset: Optional[int] = Field(default=None)
    order_by: Optional[str] = Field(default='id')
    distinct: Optional[str] = Field(default='asc')
