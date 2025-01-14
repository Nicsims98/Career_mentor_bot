"""
User model for Sage
"""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class User(Base):
    """User model"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship to chat history
    chat_history = relationship("ChatHistory", back_populates="user")

    def __repr__(self):
        return f"<User(username={self.username}, email={self.email})>"
