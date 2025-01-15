"""
Database models initialization
"""
from src.database import db

# Import models here to ensure they're registered with SQLAlchemy
from .chat_history import ChatHistory
from .user import User

