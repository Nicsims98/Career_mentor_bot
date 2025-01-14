"""
Resume analysis and skill extraction
"""

from typing import Dict, List, Optional
import re
from dataclasses import dataclass

@dataclass
class ResumeAnalysis:
    extracted_skills: List[str]
    experience_level: str
    improvement_suggestions: List[str]
    skill_gaps: Dict[str, List[str]]
    action_verbs: List[str]
    keyword_density: Dict[str, float]

class ResumeAnalyzer:
    def __init__(self):
        self.skill_patterns = self._load_skill_patterns()
        self.action_verbs = self._load_action_verbs()
        self.industry_keywords = self._load_industry_keywords()

    async def analyze_resume(
        self,
        resume_text: str,
        target_role: Optional[str] = None
    ) -> ResumeAnalysis:
        """Analyze resume content"""
        skills = self._extract_skills(resume_text)
        experience = self._determine_experience_level(resume_text)
        
        analysis = ResumeAnalysis(
            extracted_skills=skills,
            experience_level=experience,
            improvement_suggestions=self._generate_suggestions(
                resume_text,
                target_role
            ),
            skill_gaps=self._identify_skill_gaps(
                skills,
                target_role
            ) if target_role else {},
            action_verbs=self._extract_action_verbs(resume_text),
            keyword_density=self._calculate_keyword_density(resume_text)
        )
        
        return analysis

    def _extract_skills(self, text: str) -> List[str]:
        """Extract technical and soft skills from text"""
        skills = []
        
        for pattern in self.skill_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            skills.extend(match.group(0) for match in matches)
        
        return list(set(skills))

    def _determine_experience_level(self, text: str) -> str:
        """Determine experience level from resume"""
        years_exp = self._extract_years_experience(text)
        
        if years_exp < 2:
            return "entry"
        elif years_exp < 5:
            return "mid"
        else:
            return "senior"

    def _generate_suggestions(
        self,
        text: str,
        target_role: Optional[str]
    ) -> List[str]:
        """Generate resume improvement suggestions"""
        suggestions = []
        
        # Check action verb usage
        if len(self._extract_action_verbs(text)) < 5:
            suggestions.append(
                "Add more action verbs to describe your achievements"
            )
        
        # Check quantifiable results
        if not re.search(r'\d+%|\d+x', text):
            suggestions.append(
                "Add quantifiable results to demonstrate impact"
            )
        
        # Check for target role keywords
        if target_role and target_role.lower() not in text.lower():
            suggestions.append(
                f"Include keywords relevant to {target_role}"
            )
        
        return suggestions

    def _extract_action_verbs(self, text: str) -> List[str]:
        """Extract action verbs used in resume"""
        used_verbs = []
        
        for verb in self.action_verbs:
            if re.search(r'\b' + verb + r'\b', text, re.IGNORECASE):
                used_verbs.append(verb)
        
        return used_verbs

    def _calculate_keyword_density(self, text: str) -> Dict[str, float]:
        """Calculate density of industry keywords"""
        word_count = len(text.split())
        density = {}
        
        for keyword in self.industry_keywords:
            matches = len(re.findall(
                r'\b' + keyword + r'\b',
                text,
                re.IGNORECASE
            ))
            density[keyword] = matches / word_count * 100
            
        return density
