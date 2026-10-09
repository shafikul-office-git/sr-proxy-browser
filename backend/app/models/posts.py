
from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    content = Column(Text, nullable=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="posts")