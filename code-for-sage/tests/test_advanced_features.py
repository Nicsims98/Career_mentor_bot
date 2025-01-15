import pytest
from datetime import datetime, timedelta
from src.app import create_app
from src.models.learning_path import SkillLevel, LearningStatus

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_skill_analysis(client):
    """Test skill analysis endpoint"""
    test_data = {
        'user_id': 1,
        'skills': ['Python', 'React', 'SQL']
    }
    response = client.post('/api/sage/skill-analysis', json=test_data)
    assert response.status_code == 200
    assert 'analysis' in response.json
    assert 'recommended_next_steps' in response.json

def test_learning_streak(client):
    """Test learning streak updates"""
    test_data = {
        'user_id': 1,
        'skill_id': 'Python'
    }
    response = client.post('/api/sage/learning-streak', json=test_data)
    assert response.status_code == 200
    assert 'streak' in response.json
    assert 'message' in response.json

def test_career_insights(client):
    """Test career insights generation"""
    response = client.get('/api/sage/career-insights/1')
    assert response.status_code == 200
    assert 'skill_growth' in response.json
    assert 'achievement_pace' in response.json
    assert 'next_milestones' in response.json

def test_celebration_check(client):
    """Test celebration generation"""
    response = client.get('/api/sage/celebration-check')
    assert response.status_code == 200
    assert 'celebrations' in response.json