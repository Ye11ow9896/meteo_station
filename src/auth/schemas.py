from pydantic import BaseModel


class ResponseLogin(BaseModel):
    access_token: str
    user_name: str


class LoginCredentials(BaseModel):
    login: str
    password: str
