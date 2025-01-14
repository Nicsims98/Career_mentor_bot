"""
Chat history model for Sage interactions.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class ChatHistory(Base):
    """
    Structure for chat history table.
    """
    __tablename__ = 'chat_history'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    message = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    prompt_type = Column(String(50))
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationship to user table
    user = relationship("User", back_populates="chat_history")

    def __repr__(self):
        return (
            f"<ChatHistory(id={self.id}, user_id={self.user_id}, "
            f"prompt_type={self.prompt_type}, timestamp={self.timestamp})>"
        )