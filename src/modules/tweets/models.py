from sqlalchemy import Column, Integer, String, Identity, ForeignKey, UniqueConstraint
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship

from src.core.models.base import Base
from src.modules.media.models import Media
from src.modules.tweets.models import TweetLike


class Tweet(Base):
    __tablename__ = "tweets"
    # id = Column(Integer, Identity(start=1, increment=1, cycle=False), primary_key=True)
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


class TweetLike(Base):
    __tablename__ = "tweets_likes"
    __table_args__ = (UniqueConstraint("user_id", "tweet_id"),)
    # id = Column(Integer, Identity(start=1, increment=1, cycle=False), primary_key=True)
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    tweet_id = Column(ForeignKey("tweets.id", ondelete="CASCADE"), nullable=False)
    user = relationship("User", back_populates="tweets_likes")
    tweet = relationship("Tweet", back_populates="tweets_likes")