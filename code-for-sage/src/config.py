"""
Configuration settings for the application
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration."""
    
    # Error Codes
    ERROR_CODES = {
        'INVALID_INPUT': 'E001',
        'RATE_LIMIT': 'E002',
        'AUTH_ERROR': 'E003',
        'API_ERROR': 'E004',
        'DATABASE_ERROR': 'E005'
    }
    
    # Error Messages
    ERROR_MESSAGES = {
        'E001': 'Invalid input parameters',
        'E002': 'Rate limit exceeded',
        'E003': 'Authentication error',
        'E004': 'API error',
        'E005': 'Database error'
    }
    # CORS Settings
    FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:5173')
    CORS_HEADERS = [
        'Content-Type',
        'Authorization',
        'X-Requested-With',
        'Accept',
        'Origin',
        'Access-Control-Request-Method',
        'Access-Control-Request-Headers'
    ]
    
    # API Settings
    API_PREFIX = '/api'
    
    # OpenAI Settings
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    @classmethod
    def validate_config(cls):
        """Validate required configuration"""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY must be set in environment")

    # Database Settings
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'sqlite:///sage.db'  # Default to SQLite for development
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # General Settings
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    TESTING = False

class TestingConfig(Config):
    """Testing configuration."""
    DEBUG = False
    TESTING = True

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False

def get_config(env: str):
    """Retrieve the appropriate configuration class based on the environment."""
    if env == 'development':
        return DevelopmentConfig
    elif env == 'testing':
        return TestingConfig
    elif env == 'production':
        return ProductionConfig
    else:
        raise ValueError(f"Unknown environment: {env}")

# Example usage:
# config = get_config(os.getenv('FLASK_ENV', 'development'))