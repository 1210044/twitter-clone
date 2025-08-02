from sqlalchemy import Column, Integer, String, Identity, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy

from src.core.models.base import Base
from src.modules.tweets.models import TweetLike


class User(Base):
    __tablename__ = "users"
    name = Column(String(200), index=True, nullable=False)
    api_key = Column(String(200), index=True, unique=True, nullable=False)

    user_followers = relationship(
        "Follow",
        foreign_keys="[Follow.following_id]",
        back_populates="followed_user",
        cascade="all, delete-orphan"
    )
    
    user_followings = relationship(
        "Follow",
        foreign_keys="[Follow.follower_id]",
        back_populates="follower_user",
        cascade="all, delete-orphan"
    )
    
    tweets = relationship("Tweet", back_populates="author", cascade="all, delete-orphan")
    tweets_likes = relationship("TweetLike", back_populates="user", cascade="all, delete-orphan")

    followers = association_proxy("user_followers", "follower")
    followings = association_proxy("user_followings", "followed")
    likes = association_proxy(
        "tweets_likes",
        "tweet",
        creator=lambda tweet: TweetLike(tweet=tweet),
    )


class Follow(Base):
    __tablename__ = "users_follows"
    __table_args__ = (UniqueConstraint("following_id", "follower_id"),)
    
    id = Column(Integer, primary_key=True, index=True)
    following_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    follower_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    followed = relationship(
        User,
        foreign_keys=[following_id],
        back_populates="user_followers"
    )
    
    follower = relationship(
        User,
        foreign_keys=[follower_id],
        back_populates="user_followings"
    )