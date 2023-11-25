from typing import Any

from fastapi import HTTPException, status


class NotFoundException(HTTPException):
    def __init__(
        self,
        detail: str = "Not found!",
        headers: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            status.HTTP_404_NOT_FOUND, detail=detail, headers=headers
        )


class AlreadyExistsException(HTTPException):
    def __init__(
        self,
        detail: str = "Already exists!",
        headers: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            status.HTTP_409_CONFLICT, detail=detail, headers=headers
        )
