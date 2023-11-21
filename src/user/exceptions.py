from typing import Any

from fastapi import HTTPException, status


class LoginAlreadyExist(HTTPException):
    def __init__(
        self,
        detail: str = "Login already exists!",
        headers: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            status.HTTP_409_CONFLICT, detail=detail, headers=headers
        )
