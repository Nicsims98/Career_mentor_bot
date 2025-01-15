"""
OpenAI integration for Sage career mentor bot.
Handles all interactions with the OpenAI API securely.
"""

from openai import OpenAI, AuthenticationError, RateLimitError
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
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key not configured. Please set OPENAI_API_KEY environment variable.")
        
        try:
            self.client = OpenAI(api_key=self.api_key)
            # Test the API key with a minimal request
            self.client.models.list()
        except AuthenticationError:
            raise ValueError("Invalid OpenAI API key. Please check your API key configuration.")
        except RateLimitError:
            raise ValueError("OpenAI API key has exceeded its quota or rate limit")
        except Exception as e:
            raise ValueError(f"Error initializing OpenAI client: {str(e)}")
            
        self.model = "gpt-3.5-turbo"  # Using GPT-3.5-turbo as default model
        
        # Set a simple personality string for now
        self.personality = "You are Sage, a helpful career mentor chatbot. Provide friendly and professional responses to help users with their career-related questions."
        
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
        if isinstance(error, RateLimitError):
            return "The OpenAI API key has exceeded its quota. Please check your billing details at https://platform.openai.com/account/billing"
        elif isinstance(error, AuthenticationError):
            return "Invalid OpenAI API key. Please check your API key configuration."
        elif "insufficient_quota" in str(error):
            return "Your OpenAI API key has run out of credits. Please check your billing details at https://platform.openai.com/account/billing"
        else:
            return f"An error occurred while processing your request: {str(error)}"

    def chat(self, user_message: str) -> str:
        """
        Send a message to OpenAI API and get a response
        """
        try:
            print(f"Attempting to send message: {user_message}")  # Debug log
            self._rate_limit_check()
            
            # Add message to conversation history
            self.conversation_history.append({"role": "user", "content": user_message})
            
            # Ensure personality is a string
            system_message = str(self.personality) if isinstance(self.personality, dict) else self.personality
            
            # Create messages array with personality prompt and conversation history
            messages = [
                {"role": "system", "content": system_message}
            ] + self.conversation_history
            
            print(f"Sending messages to OpenAI: {messages}")  # Debug log
            
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=0.7,
                    max_tokens=1000
                )
                
                # Get the response content
                assistant_message = response.choices[0].message.content
                print(f"Received response: {assistant_message}")  # Debug log
                
                # Add assistant's response to history
                self.conversation_history.append({"role": "assistant", "content": assistant_message})
                
                return assistant_message
                
            except Exception as api_error:
                print(f"API Error Details: {str(api_error)}")  # Add detailed logging
                raise api_error
                
        except Exception as e:
            print(f"Full error details: {str(e)}")  # Add detailed logging
            return self._handle_api_error(e)

    def verify_connection(self) -> bool:
        """
        Verify that the connection to OpenAI API is working
        """
        try:
            # Test the API key with a minimal request
            models = self.client.models.list()
            print(f"Successfully connected to OpenAI API. Available models: {[model.id for model in models]}")
            return True
        except Exception as e:
            print(f"Connection test failed: {str(e)}")
            return False
