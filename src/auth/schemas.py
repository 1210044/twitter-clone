from typing import List
from pydantic import BaseModel
from src.schemas import StatusResponse


class UserIn(BaseModel):
    name: str


class UserBase(UserIn):
    id: int
    api_key: str


class User(UserBase):
    followers: List[UserBase] = []
    followings: List[UserBase] = []


class UserOut(StatusResponse):
    user: User