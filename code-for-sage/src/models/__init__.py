"""
Database models initialization
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .base import Base
from .chat_history import ChatHistory
from .user import User
import os

def init_db():
    """Initialize the database"""
    database_url = os.getenv('DATABASE_URL', 'sqlite:///sage.db')
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()
