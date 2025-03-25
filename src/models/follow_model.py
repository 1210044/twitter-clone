from sqlalchemy import Column, Integer, Identity, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from src.models.base_model import Base
from src.models.user_model import User


class Follow(Base):
    __tablename__ = "users_follows"
    __table_args__ = (UniqueConstraint("following_id", "follower_id"),)
    # id = Column(Integer, Identity(start=1, increment=1, cycle=False), primary_key=True)
    following_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    follower_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    following = relationship(
        User, foreign_keys=[following_id], back_populates="user_followings"
    )
    follower = relationship(
        User, foreign_keys=[follower_id], back_populates="user_followers"
    )