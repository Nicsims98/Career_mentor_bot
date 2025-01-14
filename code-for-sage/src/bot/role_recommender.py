"""
Role recommendation engine for career guidance
"""

from typing import List, Dict, Any
import json
from dataclasses import dataclass

@dataclass
class CareerRole:
    title: str
    description: str
    required_skills: List[str]
    salary_range: Dict[str, float]
    growth_potential: str
    job_demand: str
    remote_options: List[str]

class RoleRecommender:
    def __init__(self):
        self.roles_data = self._load_roles_data()
        self.skill_weights = {
            'exact_match': 1.0,
            'partial_match': 0.5,
            'related_match': 0.3
        }

    def _load_roles_data(self) -> Dict[str, Any]:
        """Load roles and their requirements from JSON"""
        try:
            with open('data/roles/tech_roles.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    async def get_role_recommendations(
        self,
        user_skills: List[str],
        interests: List[str],
        experience_level: str
    ) -> List[Dict[str, Any]]:
        """Get personalized role recommendations"""
        matches = []
        
        for role, details in self.roles_data.items():
            score = self._calculate_match_score(
                user_skills,
                interests,
                details
            )
            
            if score > 0.5:  # Minimum match threshold
                matches.append({
                    'role': role,
                    'match_score': score,
                    'details': details,
                    'skill_gaps': self._identify_skill_gaps(
                        user_skills,
                        details['required_skills']
                    )
                })
        
        # Sort by match score and return top 5
        matches.sort(key=lambda x: x['match_score'], reverse=True)
        return matches[:5]

    def _calculate_match_score(
        self,
        user_skills: List[str],
        interests: List[str],
        role_details: Dict
    ) -> float:
        """Calculate how well user matches a role"""
        skill_score = 0
        required_skills = role_details['required_skills']
        
        # Calculate skill match
        for skill in user_skills:
            if skill in required_skills:
                skill_score += self.skill_weights['exact_match']
            elif any(s in skill for s in required_skills):
                skill_score += self.skill_weights['partial_match']
        
        # Calculate interest match
        interest_score = sum(
            1 for interest in interests
            if interest in role_details['related_fields']
        ) / len(role_details['related_fields'])
        
        # Combine scores (60% skills, 40% interests)
        return (skill_score * 0.6) + (interest_score * 0.4)

    def _identify_skill_gaps(
        self,
        user_skills: List[str],
        required_skills: List[str]
    ) -> List[str]:
        """Identify missing skills for a role"""
        return [
            skill for skill in required_skills
            if skill not in user_skills
        ]
