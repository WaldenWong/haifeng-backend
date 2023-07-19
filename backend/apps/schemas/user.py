from pydantic import Field

from backend.apps.schemas import RWModel


class UserAddRequest(RWModel):
    username: str = Field(None, description="username")
    password: str = Field(None, description="password")
    real_name: str = Field(None, description="real_name")
    nickname: str = Field(None, description="nickname")
    phone: str = Field(None, description="phone")
