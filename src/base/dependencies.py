from typing import Annotated

from fastapi import Depends

from src.base.schemas import Pagination


def set_pagination_to_query_path():
    return Annotated[Pagination, Depends(Pagination)]
