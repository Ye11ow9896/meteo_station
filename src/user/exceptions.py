from typing import Any

from fastapi import HTTPException, status


LoginAlreadyExistException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Login already exists.",
)

BadUserLoginExceptions = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Bad user login."
)

BadUserPasswordExceptions = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Bad user password."
)
