from sqlalchemy import Column, Integer, String, Identity
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy

from src.models.base_model import Base
from src.models.tweet_like_model import TweetLike


class User(Base):
    __tablename__ = "users"
    # id = Column(Integer, Identity(start=1, increment=1, cycle=False), primary_key=True)
    name = Column(String(200), index=True, nullable=False)
    api_key = Column(String(200), index=True, nullable=False)

    user_followers = relationship(
        "Follow", foreign_keys="Follow.following_id", back_populates="following"
    )
    user_followings = relationship(
        "Follow", foreign_keys="Follow.follower_id", back_populates="follower"
    )
    tweets = relationship("Tweet", back_populates="author")
    tweets_likes = relationship("TweetLike", back_populates="user")
    followers = association_proxy("user_followers", "follower")
    followings = association_proxy("user_followings", "following")
    likes = association_proxy(
        "tweets_likes",
        "tweet",
        creator=lambda tweet: TweetLike(tweet=tweet),
    )
