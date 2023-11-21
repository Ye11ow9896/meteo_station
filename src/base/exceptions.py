from typing import Any

from fastapi import HTTPException, status


class NotFoundException(HTTPException):
    def __init__(
        self,
        detail: str = "Not found.",
        headers: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            status.HTTP_404_NOT_FOUND, detail=detail, headers=headers
        )
