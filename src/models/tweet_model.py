from sqlalchemy import Column, Integer, String, Identity, ForeignKey
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship

from src.models.base_model import Base
from src.models.media_model import Media
from src.models.tweet_like_model import TweetLike


class Tweet(Base):
    __tablename__ = "tweets"
    id = Column(Integer, Identity(start=1, increment=1, cycle=False), primary_key=True)
    content = Column(String(4000), index=True, nullable=False)
    author_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    attachments = relationship(Media, back_populates="tweet")
    author = relationship("User", back_populates="tweets")
    tweets_likes = relationship("TweetLike", back_populates="tweet")
    likes = association_proxy(
        "tweets_likes", "user", creator=lambda user: TweetLike(user=user)
    )