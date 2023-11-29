from pydantic import BaseModel


class TokenDecodedFields(BaseModel):
    expire: str
    login: str
    type: str


class LoginCredentials(BaseModel):
    login: str
    password: str
