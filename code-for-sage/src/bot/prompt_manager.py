"""
Prompt Management and Version Control for Sage
"""

from typing import Dict, Optional
import json
import os
from datetime import datetime

class PromptManager:
    def __init__(self):
        self.prompts_dir = "data/prompts/"
        self.current_version = "1.0.0"
        self.prompts = self._load_prompts()
        
    def _load_prompts(self) -> Dict:
        """Load prompt templates from file"""
        try:
            with open(f"{self.prompts_dir}prompts_v{self.current_version}.json", 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def get_prompt(
        self,
        prompt_type: str,
        variables: Optional[Dict] = None
    ) -> str:
        """Get a prompt template and fill in variables"""
        template = self.prompts.get(prompt_type, {}).get('template', '')
        if not template:
            raise ValueError(f"No prompt template found for type: {prompt_type}")
            
        if variables:
            template = template.format(**variables)
            
        return template
    
    def add_prompt(
        self,
        prompt_type: str,
        template: str,
        description: str,
        version: Optional[str] = None
    ):
        """Add or update a prompt template"""
        if version:
            self.current_version = version
            
        self.prompts[prompt_type] = {
            'template': template,
            'description': description,
            'last_modified': datetime.now().isoformat(),
            'version': self.current_version
        }
        
        self._save_prompts()
    
    def _save_prompts(self):
        """Save prompts to file"""
        os.makedirs(self.prompts_dir, exist_ok=True)
        with open(f"{self.prompts_dir}prompts_v{self.current_version}.json", 'w') as f:
            json.dump(self.prompts, f, indent=2)
