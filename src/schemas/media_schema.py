from pydantic import BaseModel

from src.schemas.status_schema import Status



class MediaBase(BaseModel):
    url: str


class MediaCreate(MediaBase):
    pass


class MediaUpdate(MediaBase):
    pass


class MediaResponse(Status):
    media_id: int


class CategoryListResponse(BaseModel):
    id: int | None = None
    name: str | None = None