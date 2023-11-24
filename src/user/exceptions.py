from typing import Any

from fastapi import HTTPException, status


BadUserLoginExceptions = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Bad user login."
)

BadUserPasswordException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Bad user password."
)
