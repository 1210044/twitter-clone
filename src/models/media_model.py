from sqlalchemy import Column, Integer, String, Identity, ForeignKey
from sqlalchemy.orm import relationship

from src.models.base_model import Base


class Media(Base):
    __tablename__ = "tweets_medias"
    id = Column(Integer, Identity(start=1, increment=1, cycle=False), primary_key=True)
    url = Column(String(2048), nullable=False)
    tweet_id = Column(Integer, ForeignKey("tweets.id"), nullable=True)
    tweet = relationship("Tweet", back_populates="attachments")
