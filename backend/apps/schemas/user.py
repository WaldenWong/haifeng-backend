from pydantic import Field

from backend.apps.schemas.request import FilterRequest


class AddRequest(FilterRequest):
    username: str = Field(None, description="username")
    password: str = Field(None, description="password")
    realname: str = Field(None, description="realname")
    nickname: str = Field(None, description="nickname")
    email: str = Field(None, description="email")
    phone: str = Field(None, description="phone")
