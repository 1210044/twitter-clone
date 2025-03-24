from typing import List
from pydantic import BaseModel, ConfigDict
from src.schemas.status_schema import Status


class UserIn(BaseModel):
    name: str


class UserBase(UserIn):
    model_config = ConfigDict(from_attributes=True)
    id: int


class User(UserBase):
    followers: List[UserBase] = []
    followings: List[UserBase] = []


class UserOut(Status):
    user: User
