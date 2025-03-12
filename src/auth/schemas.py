from typing import List
from pydantic import BaseModel, ConfigDict
from src.schemas import StatusResponse


class UserIn(BaseModel):
    name: str


class UserBase(UserIn):
    model_config = ConfigDict(from_attributes=True)
    id: int
    api_key: str


class User(UserBase):
    followers: List[UserBase] = []
    followings: List[UserBase] = []


class UserOut(StatusResponse):
    user: User