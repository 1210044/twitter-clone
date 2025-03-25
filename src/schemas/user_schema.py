from typing import List
from pydantic import BaseModel, ConfigDict
from src.schemas.status_schema import Status


class UserCreate(BaseModel):
    name: str


class UserBase(UserCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int


class UserUpdate(UserBase):
    pass


class User(UserBase):
    followers: List[UserBase] = []
    followings: List[UserBase] = []


class UserOut(Status):
    user: User
