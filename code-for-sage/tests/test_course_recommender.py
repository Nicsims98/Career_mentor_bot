"""
Tests for the enhanced course recommender
"""

import pytest
from src.bot.course_recommender import CourseRecommender, LearningPace
import asyncio

@pytest.fixture
def recommender():
    return CourseRecommender()

def test_time_breakdown():
    """Test time breakdown calculations"""
    recommender = CourseRecommender()
    
    # Test different scenarios
    scenarios = [
        {
            'hours': 5,
            'pace': LearningPace.RELAXED
        },
        {
            'hours': 10,
            'pace': LearningPace.MODERATE
        },
        {
            'hours': 20,
            'pace': LearningPace.INTENSIVE
        }
    ]
    
    for scenario in scenarios:
        breakdown = recommender._generate_time_breakdown(
            scenario['hours'],
            scenario['pace']
        )
        
        print(f"\nTesting scenario: {scenario['hours']} hours, {scenario['pace'].value} pace")
        print("Time Breakdown:")
        print(json.dumps(breakdown, indent=2))
        
        assert breakdown['weekly_breakdown']
        assert breakdown['estimated_milestones']

async def test_course_recommendations():
    """Test course recommendation generation"""
    recommender = CourseRecommender()
    
    test_data = {
        'user_skills': ['Python', 'HTML'],
        'career_goal': 'Full Stack Developer',
        'available_hours': 10,
        'learning_pace': LearningPace.MODERATE,
        'commitments': ['Full-time job', 'Family']
    }
    
    recommendations = await recommender.get_personalized_courses(
        user_skills=test_data['user_skills'],
        career_goal=test_data['career_goal'],
        available_hours_per_week=test_data['available_hours'],
        learning_pace=test_data['learning_pace'],
        current_commitments=test_data['commitments']
    )
    
    print("\nTesting Course Recommendations:")
    print(json.dumps(recommendations, indent=2))
    
    assert recommendations['success']
    assert 'schedule_analysis' in recommendations
    assert 'recommendations' in recommendations
    assert 'time_commitment_breakdown' in recommendations

if __name__ == "__main__":
    # Run async tests
    asyncio.run(test_course_recommendations())
    
    # Run sync tests
    test_time_breakdown()