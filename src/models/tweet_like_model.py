from sqlalchemy import Column, Integer, Identity, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from src.models.base_model import Base


class TweetLike(Base):
    __tablename__ = "tweets_likes"
    __table_args__ = (UniqueConstraint("user_id", "tweet_id"),)
    # id = Column(Integer, Identity(start=1, increment=1, cycle=False), primary_key=True)
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    tweet_id = Column(ForeignKey("tweets.id", ondelete="CASCADE"), nullable=False)
    user = relationship("User", back_populates="tweets_likes")
    tweet = relationship("Tweet", back_populates="tweets_likes")