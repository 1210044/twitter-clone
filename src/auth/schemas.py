from typing import List
from pydantic import BaseModel, ConfigDict
from src.schemas import StatusResponse


class ApiKey(BaseModel):
    api_key: str


class UserIn(BaseModel):
    name: str


class UserBase(UserIn):
    model_config = ConfigDict(from_attributes=True)
    id: int


class User(UserBase):
    followers: List[UserBase] = []
    followings: List[UserBase] = []


class UserOut(StatusResponse):
    user: User