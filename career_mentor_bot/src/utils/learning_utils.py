"""
Enhanced utility functions for learning management
"""

from typing import List, Dict
from datetime import datetime, timedelta

class LearningUtils:
    def __init__(self):
        self.energy_patterns = {
            'morning': {'peak_hours': ['06:00', '10:00'], 'best_for': ['Deep learning', 'Complex topics']},
            'afternoon': {'peak_hours': ['14:00', '17:00'], 'best_for': ['Practice', 'Reviews']},
            'evening': {'peak_hours': ['19:00', '22:00'], 'best_for': ['Light reading', 'Planning']}
        }

    def calculate_learning_velocity(
        self,
        past_completions: List[Dict],
        target_hours: int
    ) -> Dict:
        """
        Calculate learning speed and project completion dates
        """
        if not past_completions:
            return {
                'estimated_pace': 'No historical data',
                'projected_completion': None
            }

        # Calculate average completion rate
        total_hours = sum(item['hours_spent'] for item in past_completions)
        total_topics = len(past_completions)
        
        if total_topics == 0:
            return {
                'average_hours_per_topic': 0,
                'estimated_completion_weeks': 0,
                'confidence_level': 'Low - No data'
            }
            
        avg_hours_per_topic = total_hours / total_topics

        return {
            'average_hours_per_topic': avg_hours_per_topic,
            'estimated_completion_weeks': round(target_hours / avg_hours_per_topic * 1.5, 1),
            'confidence_level': self._calculate_confidence(past_completions)
        }

    def generate_milestone_checklist(
        self,
        course_length: int,
        difficulty: str
    ) -> List[Dict]:
        """
        Create milestone checklist with achievements
        """
        milestones = []
        checkpoint_intervals = self._get_checkpoint_intervals(difficulty)
        
        current_date = datetime.now()
        
        for week in range(0, course_length, checkpoint_intervals):
            milestone_date = current_date + timedelta(weeks=week)
            milestones.append({
                'week': week,
                'target_date': milestone_date.strftime('%Y-%m-%d'),
                'checkpoint_type': self._get_checkpoint_type(week, course_length),
                'achievements': self._generate_achievements(week, difficulty),
                'review_materials': self._suggest_review_materials(week, difficulty)
            })
        
        return milestones

    def analyze_learning_style(
        self,
        preferences: Dict
    ) -> Dict:
        """
        Analyze learning style and suggest optimal approaches
        """
        style_scores = {
            'visual': 0,
            'auditory': 0,
            'kinesthetic': 0,
            'reading/writing': 0
        }
        
        # Score each learning style based on preferences
        for pref in preferences.get('preferred_methods', []):
            if 'watch' in pref or 'diagram' in pref:
                style_scores['visual'] += 1
            if 'listen' in pref or 'discuss' in pref:
                style_scores['auditory'] += 1
            if 'practice' in pref or 'build' in pref:
                style_scores['kinesthetic'] += 1
            if 'read' in pref or 'write' in pref:
                style_scores['reading/writing'] += 1

        dominant_style = max(style_scores.items(), key=lambda x: x[1])[0]
        
        return {
            'dominant_style': dominant_style,
            'style_breakdown': style_scores,
            'recommended_methods': self._get_learning_methods(dominant_style),
            'tool_suggestions': self._suggest_learning_tools(dominant_style)
        }

    def create_spaced_repetition_schedule(
        self,
        topics: List[str],
        start_date: datetime
    ) -> Dict:
        """
        Create a spaced repetition schedule for optimal learning
        """
        schedule = {}
        intervals = [1, 3, 7, 14, 30]  # Days between reviews
        
        for topic in topics:
            topic_schedule = []
            current_date = start_date
            
            for interval in intervals:
                review_date = current_date + timedelta(days=interval)
                topic_schedule.append({
                    'review_date': review_date.strftime('%Y-%m-%d'),
                    'review_type': self._get_review_type(interval),
                    'estimated_duration': self._get_review_duration(interval)
                })
                current_date = review_date
                
            schedule[topic] = topic_schedule
            
        return schedule

    def _calculate_confidence(self, completions: List[Dict]) -> str:
        """Calculate confidence level in estimates"""
        if len(completions) < 3:
            return 'Low - Limited historical data'
        
        consistency = self._check_completion_consistency(completions)
        return 'High' if consistency > 0.7 else 'Medium'

    def _get_checkpoint_intervals(self, difficulty: str) -> int:
        """Get appropriate intervals between checkpoints"""
        intervals = {
            'beginner': 1,
            'intermediate': 2,
            'advanced': 3
        }
        return intervals.get(difficulty.lower(), 2)

    def _get_checkpoint_type(self, week: int, total_weeks: int) -> str:
        """Determine type of checkpoint based on progress"""
        if week == 0:
            return 'Initial Assessment'
        elif week == total_weeks - 1:
            return 'Final Review'
        else:
            return 'Progress Check'

    def _generate_achievements(self, week: int, difficulty: str) -> List[str]:
        """Generate appropriate achievements for milestone"""
        base_achievements = {
            'beginner': ['Complete tutorial', 'Submit basic project'],
            'intermediate': ['Build complex feature', 'Pass technical quiz'],
            'advanced': ['Create full project', 'Technical presentation']
        }
        return base_achievements.get(difficulty.lower(), ['General review'])

    def _suggest_review_materials(self, week: int, difficulty: str) -> List[str]:
        """Suggest review materials based on progress"""
        materials = {
            'beginner': ['Practice exercises', 'Video tutorials'],
            'intermediate': ['Documentation', 'Code reviews'],
            'advanced': ['Research papers', 'Architecture reviews']
        }
        return materials.get(difficulty.lower(), ['General materials'])

    def _get_learning_methods(self, style: str) -> List[str]:
        """Get recommended learning methods for learning style"""
        methods = {
            'visual': ['Diagrams', 'Video tutorials', 'Mind maps'],
            'auditory': ['Podcasts', 'Group discussions', 'Audio books'],
            'kinesthetic': ['Coding exercises', 'Project work', 'Labs'],
            'reading/writing': ['Documentation', 'Blog posts', 'Written exercises']
        }
        return methods.get(style, ['Mixed methods'])

    def _suggest_learning_tools(self, style: str) -> List[str]:
        """Suggest learning tools based on style"""
        tools = {
            'visual': ['YouTube tutorials', 'Diagram tools', 'Screen recordings'],
            'auditory': ['Educational podcasts', 'Discussion forums', 'Study groups'],
            'kinesthetic': ['Interactive coding platforms', 'GitHub projects', 'Hackathons'],
            'reading/writing': ['Documentation sites', 'Technical blogs', 'Note-taking apps']
        }
        return tools.get(style, ['General learning platforms'])

    def _get_review_type(self, interval: int) -> str:
        """Get review type based on interval"""
        if interval == 1:
            return 'Immediate Review'
        elif interval == 3:
            return 'Short-term Review'
        elif interval == 7:
            return 'Weekly Review'
        elif interval == 14:
            return 'Bi-weekly Review'
        elif interval == 30:
            return 'Monthly Review'
        else:
            return 'General Review'

    def _get_review_duration(self, interval: int) -> str:
        """Estimate review duration based on interval"""
        if interval == 1:
            return '15 minutes'
        elif interval == 3:
            return '30 minutes'
        elif interval == 7:
            return '1 hour'
        elif interval == 14:
            return '1.5 hours'
        elif interval == 30:
            return '2 hours'
        else:
            return 'Varies'

    def _check_completion_consistency(self, completions: List[Dict]) -> float:
        """Check consistency of completion times"""
        if len(completions) < 2:
            return 0.0
        
        time_diffs = []
        for i in range(1, len(completions)):
            time_diff = (completions[i]['completion_date'] - completions[i-1]['completion_date']).days
            time_diffs.append(time_diff)
        
        avg_diff = sum(time_diffs) / len(time_diffs)
        variance = sum((x - avg_diff) ** 2 for x in time_diffs) / len(time_diffs)
        consistency = 1 / (1 + variance)
        
        return consistency