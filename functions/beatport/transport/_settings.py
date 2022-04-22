from pydantic import BaseSettings


class LoginSettings(BaseSettings):
    username: str
    password: str
    remember: bool = False
