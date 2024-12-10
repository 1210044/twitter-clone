from typing import List
from pydantic import BaseModel, field_validator

from src.logger import logger
from src.schemas import StatusResponseTrue
from src.auth.schemas import UserBase


class TweetIn(BaseModel):
    tweet_data: str
    tweet_media_ids: List[int] = []


class TweetOut(StatusResponseTrue):
    tweet_id: int


class Tweet(BaseModel):
    id: int
    content: str
    attachments: List[str] = []
    author: UserBase
    likes: List[UserBase] = []

    @field_validator('attachments', mode='before')
    @classmethod
    def get_urls(cls, values):
        if isinstance(values, list):
            return [media.url for media in values if hasattr(media, 'url')]
        return values


class TweetsOut(StatusResponseTrue):
    tweets: List[Tweet] = []