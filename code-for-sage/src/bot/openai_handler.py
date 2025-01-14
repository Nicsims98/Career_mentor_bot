"""
OpenAI integration for Sage career mentor bot.
Handles all interactions with the OpenAI API securely.
"""

from openai import OpenAI
from dotenv import load_dotenv
import os
import time
from typing import Dict, Optional, List
from .personality import SAGE_PERSONALITY
from .performance_monitor import PerformanceMonitor
from .prompt_manager import PromptManager
from .safety_checker import SafetyChecker

# Load environment variables
load_dotenv()

class SageAI:
    def __init__(self):
        # Securely get API key from environment
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4"
        self.personality = SAGE_PERSONALITY
        self.conversation_history = []
        self.last_api_call = 0
        self.min_time_between_calls = 1  # Minimum seconds between API calls
        
        # Initialize new components
        self.performance_monitor = PerformanceMonitor()
        self.prompt_manager = PromptManager()
        self.safety_checker = SafetyChecker()
        
    def _rate_limit_check(self):
        """Ensure we don't exceed API rate limits"""
        current_time = time.time()
        time_since_last_call = current_time - self.last_api_call
        
        if time_since_last_call < self.min_time_between_calls:
            time.sleep(self.min_time_between_calls - time_since_last_call)
            
        self.last_api_call = time.time()

    def _handle_api_error(self, error: Exception) -> str:
        """Handle different types of API errors"""
        if "Rate limit" in str(error):
            return self.personality['error_messages']['rate_limit']
        elif "Invalid API key" in str(error):
            return self.personality['error_messages']['api_error']
        else:
            return f"I apologize, but I encountered an error: {str(error)}"

    def _update_conversation_history(
        self,
        role: str,
        content: str,
        max_history: int = 10
    ):
        """Maintain conversation history"""
        # Add new message
        self.conversation_history.append({
            'role': role,
            'content': content,
            'timestamp': time.time()
        })
        
        # Keep only recent messages, but ensure system messages are preserved
        if len(self.conversation_history) > max_history:
            system_messages = [msg for msg in self.conversation_history if msg['role'] == 'system']
            other_messages = [msg for msg in self.conversation_history if msg['role'] != 'system'][-max_history:]
            self.conversation_history = system_messages + other_messages
        
    def create_base_prompt(self):
        """Creates the base personality prompt for Sage"""
        return f"""You are {self.personality['name']}, a career mentor with expertise in tech and professional development.
        Your communication style is {self.personality['traits']['communication_style']}.
        Always maintain a supportive and encouraging tone while providing specific, actionable advice."""

    def create_specialized_prompt(self, prompt_type, user_input, user_context=None):
        """Creates specialized prompts based on the type of career guidance needed"""
        base_prompt = self.create_base_prompt()
        
        prompts = {
            'skill_analysis': f"""
                {base_prompt}
                
                Analyze the following skills and provide:
                1. Current market demand for each skill
                2. Complementary skills to learn
                3. Specific learning resources
                4. Potential career paths
                
                User's skills: {user_input}
                Context: {user_context if user_context else 'No previous context'}
                
                Format your response with emojis and clear sections.
            """,
            
            'career_path': f"""
                {base_prompt}
                
                Based on the user's interests and background, suggest career paths:
                1. 3-5 relevant job titles with descriptions
                2. Required skills for each role
                3. Typical career progression
                4. Salary ranges (entry to senior level)
                5. Learning roadmap
                
                User's background: {user_input}
                Context: {user_context if user_context else 'No previous context'}
                
                Use bullet points and emojis for clarity.
            """,
            
            'course_recommendation': f"""
                {base_prompt}
                
                Recommend learning resources based on the user's goals:
                1. Top 3 most relevant courses/certifications
                2. Why each resource is recommended
                3. Estimated time commitment
                4. Prerequisites if any
                5. Expected outcomes
                
                User's learning goals: {user_input}
                Context: {user_context if user_context else 'No previous context'}
                
                Format with clear sections and encouraging language.
            """,
            
            'interview_prep': f"""
                {base_prompt}
                
                Provide interview preparation guidance:
                1. Common interview questions for the role
                2. How to structure responses (STAR method)
                3. Technical concepts to review
                4. Questions to ask the interviewer
                5. Preparation tips
                
                Role interested in: {user_input}
                Context: {user_context if user_context else 'No previous context'}
                
                Include examples and confidence-building tips.
            """,
            
            'resume_advice': f"""
                {base_prompt}
                
                Provide resume optimization advice:
                1. Key skills to highlight
                2. Action verbs to use
                3. Industry-specific tips
                4. Common mistakes to avoid
                5. ATS optimization suggestions
                
                Current role/target role: {user_input}
                Context: {user_context if user_context else 'No previous context'}
                
                Include specific examples and formatting tips.
            """,
            
            'industry_insights': f"""
                {base_prompt}
                
                Provide current industry insights:
                1. Latest trends and technologies
                2. Growing areas of opportunity
                3. Required skills for future success
                4. Industry challenges and solutions
                5. Notable companies and their focus areas
                
                Industry of interest: {user_input}
                Context: {user_context if user_context else 'No previous context'}
                
                Include recent developments and future predictions.
            """,
            
            'learning_schedule': f"""
                {base_prompt}
                
                Create a personalized learning schedule considering:
                1. Available time: {user_input} hours per week
                2. Current commitments: {user_context if user_context else 'No commitments specified'}
                3. Learning style preferences
                4. Energy levels throughout the day
                5. Optimal study patterns
                
                Provide:
                - Detailed weekly schedule
                - Study session recommendations
                - Break patterns
                - Progress tracking suggestions
                
                Format with clear sections and time blocks.
            """,
            
            'course_pacing': f"""
                {base_prompt}
                
                Analyze this learning scenario:
                User Input: {user_input}
                Context: {user_context if user_context else 'No additional context'}
                
                Provide:
                1. Recommended pacing for the course
                2. Time allocation per week
                3. Milestones to track progress
                4. Adjustments for different learning speeds
                
                Use clear sections and encouraging language.
            """
        }
        
        return prompts.get(prompt_type, base_prompt)

    async def get_quick_response(
        self,
        user_input: str,
        context: Optional[str] = None
    ) -> Dict:
        """
        Get a quick response for simple questions
        """
        try:
            self._rate_limit_check()
            
            prompt = f"""
            {self.create_base_prompt()}
            
            Provide a concise, helpful response to:
            {user_input}
            
            Context (if any): {context if context else 'No additional context'}
            
            Keep the response brief but informative.
            """
            
            completion = self.client.chat.completions.create(
                model=self.model,
                store=True,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": user_input}
                ]
            )
            
            response = completion.choices[0].message.content
            
            # Update conversation history
            self._update_conversation_history('user', user_input)
            self._update_conversation_history('assistant', response)
            
            return {
                'success': True,
                'response': response,
                'context_preserved': True
            }
            
        except Exception as e:
            error_message = self._handle_api_error(e)
            return {
                'success': False,
                'error': error_message,
                'context_preserved': False
            }

    async def get_career_advice(
        self,
        prompt_type: str,
        user_input: str,
        context: Optional[str] = None,
        user_id: Optional[str] = None,
        ip: Optional[str] = None
    ) -> Dict:
        """Get specialized career advice from OpenAI"""
        try:
            self._rate_limit_check()
            
            prompt = self.create_specialized_prompt(prompt_type, user_input, context)
            
            # Include relevant conversation history
            messages = [
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_input}
            ]
            
            # Add recent relevant history if available
            relevant_history = self._get_relevant_history(prompt_type)
            if relevant_history:
                messages[0]["content"] += f"\nRelevant context: {relevant_history}"
            
            completion = self.client.chat.completions.create(
                model=self.model,
                store=True,
                messages=messages
            )
            
            response = completion.choices[0].message.content
            
            # Update conversation history
            self._update_conversation_history('user', user_input)
            self._update_conversation_history('assistant', response)
            
            return response
            
        except Exception as e:
            return self._handle_api_error(e)

    def _get_relevant_history(self, prompt_type: str) -> Optional[str]:
        """Get relevant conversation history for context"""
        relevant_messages = []
        
        for msg in reversed(self.conversation_history[-5:]):  # Look at last 5 messages
            if prompt_type.lower() in msg['content'].lower():
                relevant_messages.append(f"{msg['role']}: {msg['content']}")
                
        return "\n".join(relevant_messages) if relevant_messages else None

    def get_conversation_summary(self) -> Dict:
        """Get a summary of the conversation history"""
        return {
            'message_count': len(self.conversation_history),
            'topics_discussed': self._extract_topics(),
            'last_interaction': self.conversation_history[-1] if self.conversation_history else None
        }

    def _extract_topics(self) -> List[str]:
        """Extract main topics from conversation history"""
        topics = set()
        for msg in self.conversation_history:
            if 'career' in msg['content'].lower():
                topics.add('career guidance')
            if 'course' in msg['content'].lower():
                topics.add('course recommendations')
            if 'skill' in msg['content'].lower():
                topics.add('skill assessment')
        return list(topics)