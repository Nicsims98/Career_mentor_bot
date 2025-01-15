"""
Chat history model for Sage interactions.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from src.database import db
from src.models.user import User  # Import the User model

class ChatHistory(db.Model):
    """
    Structure for chat history table.
    """
    __tablename__ = 'chat_history'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'))
    message = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=False)
    prompt_type = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to user table
    user = relationship("User", back_populates="chat_history")