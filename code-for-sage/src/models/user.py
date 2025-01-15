"""
User model for Sage
"""

from src.database import db
from sqlalchemy.orm import relationship

class User(db.Model):
    """User model"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=True)
    work_type = db.Column(db.String(50), nullable=True)
    location = db.Column(db.String(100), nullable=True)
    job_preference = db.Column(db.String(100), nullable=True)
    skills = db.Column(db.Text, nullable=True)  # Store as comma-separated values
    interests = db.Column(db.Text, nullable=True)  # Store as comma-separated values
    education = db.Column(db.Text, nullable=True) # Store as comma-separated values
    work_experience = db.Column(db.Text, nullable=True) # Store as comma-separated values
    short_term_career_goals = db.Column(db.Text, nullable=True)
    long_term_career_goals = db.Column(db.Text, nullable=True)

    # Add the relationship to ChatHistory
    chat_history = relationship("ChatHistory", back_populates="user")

    def __repr__(self):
        return f"<User(username={self.email})>"
