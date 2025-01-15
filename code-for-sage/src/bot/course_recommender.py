from typing import List, Dict, Any
from datetime import datetime, timedelta
from enum import Enum


class LearningPace(Enum):
    SLOW = "slow"
    MODERATE = "moderate"
    FAST = "fast"


class JobMatchLevel(Enum):
    ENTRY = "entry"
    INTERMEDIATE = "intermediate"
    SENIOR = "senior"

class CourseRecommender:
    def __init__(self):
        # Initialize any necessary variables or configurations here
        self.categories = {
            'programming': {
                'topics': ['python', 'java', 'c++'],
                'levels': {
                    'beginner': {'duration_weeks': 4},
                    'intermediate': {'duration_weeks': 8},
                    'advanced': {'duration_weeks': 12}
                }
            },
            'data_science': {
                'topics': ['machine learning', 'data analysis', 'statistics'],
                'levels': {
                    'beginner': {'duration_weeks': 6},
                    'intermediate': {'duration_weeks': 10},
                    'advanced': {'duration_weeks': 14}
                }
            }
        }

    def calculate_job_readiness_date(self, weeks_needed: int) -> str:
        """
        Calculate estimated date of job readiness
        """
        target_date = datetime.now() + timedelta(weeks=weeks_needed)
        return target_date.strftime('%Y-%m-%d')

    def _generate_time_breakdown(self, available_hours: int, pace: str) -> Dict[str, float]:
        """
        Generate a detailed time breakdown for learning based on available hours and pace
        """
        pace_multiplier = {
            'slow': 0.5,
            'moderate': 1.0,
            'fast': 1.5
        }.get(pace, 1.0)
        
        total_hours = available_hours * pace_multiplier
        weekly_hours = total_hours / 7
        
        return {
            'total_hours': total_hours,
            'weekly_hours': weekly_hours,
            'daily_hours': weekly_hours / 7
        }

    async def get_personalized_courses(self, user_skills: List[str], career_goal: str, available_hours_per_week: int, learning_pace: str, current_commitments: List[str], preferred_learning_style: str) -> Dict[str, Any]:
        """
        Get personalized course recommendations based on user input
        """
        # Placeholder for actual recommendation logic
        recommendations = [
            {
                'course_name': 'Introduction to Python',
                'provider': 'Coursera',
                'duration_weeks': 6,
                'weekly_hours': 5,
                'description': 'Learn the basics of Python programming.'
            },
            {
                'course_name': 'Data Science Fundamentals',
                'provider': 'edX',
                'duration_weeks': 10,
                'weekly_hours': 8,
                'description': 'An introduction to data science concepts and techniques.'
            }
        ]
        
        # Calculate job readiness date based on the longest course duration
        max_duration_weeks = max(course['duration_weeks'] for course in recommendations)
        job_readiness_date = self.calculate_job_readiness_date(max_duration_weeks)
        
        return {
            'recommendations': recommendations,
            'job_readiness_date': job_readiness_date
        }

    async def analyze_user_schedule(self, available_hours_per_week: int, preferred_pace: str, current_commitments: List[str]) -> Dict[str, Any]:
        """
        Analyze user's schedule and provide a learning plan
        """
        time_breakdown = self._generate_time_breakdown(available_hours_per_week, preferred_pace)
        
        # Placeholder for actual analysis logic
        analysis = {
            'time_breakdown': time_breakdown,
            'commitments': current_commitments,
            'suggestions': 'Adjust your schedule to allocate more consistent study hours.'
        }
        
        return analysis

    async def match_jobs_to_skills(self, user_skills: List[str], job_listings: List[Dict], experience_level: JobMatchLevel = JobMatchLevel.ENTRY) -> Dict[str, Any]:
        """
        Match scraped job listings to user's skills and learning path
        """
        try:
            # Calculate skill match percentages
            matched_jobs = []
            for job in job_listings:
                match_score = self._calculate_job_match(
                    user_skills,
                    job.get('required_skills', []),
                    experience_level
                )
                
                if match_score['match_percentage'] > 50:  # Only include good matches
                    matched_jobs.append({
                        'job_title': job.get('title'),
                        'company': job.get('company'),
                        'match_score': match_score,
                        'missing_skills': match_score['missing_skills'],
                        'learning_time_estimate': self._estimate_skill_acquisition_time(
                            match_score['missing_skills']
                        )
                    })
            
            # Sort by match percentage
            matched_jobs.sort(key=lambda x: x['match_score']['match_percentage'], reverse=True)
            
            return {
                'success': True,
                'matched_jobs': matched_jobs[:5],  # Top 5 matches
                'total_matches': len(matched_jobs)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def _calculate_job_match(self, user_skills: List[str], required_skills: List[str], experience_level: JobMatchLevel) -> Dict[str, Any]:
        """
        Calculate how well user's skills match job requirements
        """
        # Normalize skills for comparison
        user_skills_normalized = [skill.lower() for skill in user_skills]
        required_skills_normalized = [skill.lower() for skill in required_skills]
        
        # Find matching and missing skills
        matching_skills = [
            skill for skill in required_skills_normalized
            if skill in user_skills_normalized
        ]
        
        missing_skills = [
            skill for skill in required_skills_normalized
            if skill not in user_skills_normalized
        ]
        
        # Calculate match percentage with experience level weighting
        base_match = len(matching_skills) / len(required_skills) * 100
        
        # Adjust match based on experience level
        level_adjustments = {
            JobMatchLevel.ENTRY: 1.2,  # More forgiving for entry level
            JobMatchLevel.INTERMEDIATE: 1.0,
            JobMatchLevel.SENIOR: 0.8  # Stricter for senior roles
        }
        
        adjusted_match = base_match * level_adjustments[experience_level]
        
        return {
            'match_percentage': round(min(adjusted_match, 100), 1),
            'matching_skills': matching_skills,
            'missing_skills': missing_skills,
            'experience_level': experience_level.value
        }

    def _estimate_skill_acquisition_time(self, missing_skills: List[str]) -> Dict[str, Any]:
        """
        Estimate time needed to acquire missing skills
        """
        total_weeks = 0
        skill_breakdown = {}
        
        for skill in missing_skills:
            # Find category containing the skill
            for category, data in self.categories.items():
                if skill.lower() in [t.lower() for t in data['topics']]:
                    weeks = data['levels']['beginner']['duration_weeks']
                    total_weeks += weeks
                    skill_breakdown[skill] = {
                        'estimated_weeks': weeks,
                        'category': category
                    }
                    break
            else:
                # Default if skill not found in categories
                total_weeks += 4
                skill_breakdown[skill] = {
                    'estimated_weeks': 4,
                    'category': 'general'
                }
        
        return {
            'total_weeks': total_weeks,
            'skill_breakdown': skill_breakdown,
            'recommended_order': self._suggest_learning_order(skill_breakdown)
        }

    def _suggest_learning_order(self, skill_breakdown: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Suggest optimal order for learning missing skills
        """
        # Sort skills by estimated time (shorter first) and dependencies
        ordered_skills = []
        skills = list(skill_breakdown.items())
        
        # Sort by weeks needed
        skills.sort(key=lambda x: x[1]['estimated_weeks'])
        
        for skill, details in skills:
            ordered_skills.append({
                'skill': skill,
                'weeks_needed': details['estimated_weeks'],
                'category': details['category'],
                'suggested_resources': self._get_skill_resources(
                    skill,
                    details['category']
                )
            })
        
        return ordered_skills

    def _get_skill_resources(self, skill: str, category: str) -> List[str]:
        """
        Get recommended resources for a specific skill
        """
        # This could be expanded with actual course data
        return [
            f"Online course: {skill} Fundamentals",
            f"Practice platform for {skill}",
            f"Documentation and tutorials for {skill}"
        ]

    async def get_career_roadmap(self, current_skills: List[str], target_job: Dict[str, Any], available_hours: int) -> Dict[str, Any]:
        """
        Create a complete roadmap from current skills to target job
        """
        try:
            # Calculate skill gaps
            match_analysis = self._calculate_job_match(
                current_skills,
                target_job.get('required_skills', []),
                JobMatchLevel.ENTRY
            )
            
            # Estimate learning timeline
            timeline = self._estimate_skill_acquisition_time(
                match_analysis['missing_skills']
            )
            
            # Get course recommendations for missing skills
            courses = await self.get_personalized_courses(
                current_skills,
                target_job.get('title', ''),
                available_hours,
                'moderate',
                []
            )
            
            return {
                'success': True,
                'current_match': match_analysis,
                'learning_timeline': timeline,
                'recommended_courses': courses,
                'estimated_job_readiness': self._calculate_readiness_date(
                    timeline['total_weeks']
                )
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def _calculate_readiness_date(self, weeks_needed: int) -> str:
        """
        Calculate estimated date of job readiness
        """
        target_date = datetime.now() + timedelta(weeks=weeks_needed)
        return target_date.strftime('%Y-%m-%d')