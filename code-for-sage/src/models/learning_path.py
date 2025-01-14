"""
Advanced learning path tracking for personalized career guidance
"""

from datetime import datetime
import enum

class SkillLevel(enum.Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class LearningStatus(enum.Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    MASTERED = "mastered"

class UserSkillProgress:
    def __init__(self, user_id, skill_name, current_level, confidence_score, last_practiced=None, learning_streak=0):
        self.id = None  # This would be set by the system if needed
        self.user_id = user_id
        self.skill_name = skill_name
        self.current_level = SkillLevel(current_level)
        self.confidence_score = confidence_score
        self.last_practiced = last_practiced if last_practiced else datetime.utcnow()
        self.learning_streak = learning_streak

    def __repr__(self):
        return (f"<UserSkillProgress(user_id={self.user_id}, skill_name={self.skill_name}, "
                f"current_level={self.current_level}, confidence_score={self.confidence_score}, "
                f"last_practiced={self.last_practiced}, learning_streak={self.learning_streak})>")

class CareerMilestone:
    def __init__(self, user_id, milestone_type, description, achieved_date=None, celebration_sent=False):
        self.id = None  # This would be set by the system if needed
        self.user_id = user_id
        self.milestone_type = milestone_type
        self.description = description
        self.achieved_date = achieved_date if achieved_date else datetime.utcnow()
        self.celebration_sent = celebration_sent

    def __repr__(self):
        return (f"<CareerMilestone(user_id={self.user_id}, milestone_type={self.milestone_type}, "
                f"description={self.description}, achieved_date={self.achieved_date}, "
                f"celebration_sent={self.celebration_sent})>")