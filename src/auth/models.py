from sqlalchemy import Column, Integer, String, Identity, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy

from src.models import Base
from src.tweets.models import TweetLike


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, Identity(start=1, increment=1, cycle=False), primary_key=True)
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


class Follow(Base):
    __tablename__ = "users_follows"
    __table_args__ = (UniqueConstraint("following_id", "follower_id"),)
    id = Column(Integer, Identity(start=1, increment=1, cycle=False), primary_key=True)
    following_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    follower_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    following = relationship(
        "User", foreign_keys=[following_id], back_populates="user_followings"
    )
    follower = relationship(
        "User", foreign_keys=[follower_id], back_populates="user_followers"
    )
