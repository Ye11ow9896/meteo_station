from fastapi import HTTPException, status

BadLoginExceptions = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Bad login!"
)

BadPasswordException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Bad password!"
)
