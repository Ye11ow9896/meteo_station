from fastapi import HTTPException, status

BadLoginExceptions = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Bad login!"
)

BadPasswordException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Bad password!"
)

UnauthorizedException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Unauthorized!'
)

TokenExpiredException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Token has expired!'
)
