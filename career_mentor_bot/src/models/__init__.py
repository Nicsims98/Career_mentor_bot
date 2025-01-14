"""
Data Models Package
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from .base import Base
from .chat_history import ChatHistory
from config import Config

# Create engine
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)

# Create session factory
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

# Create all tables
def init_db():
    Base.metadata.create_all(engine)
