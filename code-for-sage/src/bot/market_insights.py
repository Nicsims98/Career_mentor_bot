"""
Market insights and analytics for career guidance
"""

import os
import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Any
import aiohttp
from dataclasses import dataclass

class MarketInsights:
    def __init__(self):
        # API keys
        self.coursera_api_key = os.getenv('COURSERA_API_KEY')
        self.udemy_api_key = os.getenv('UDEMY_API_KEY')
        self.hackernews_api_key = os.getenv('HACKERNEWS_API_KEY')
        self.meetup_api_key = os.getenv('MEETUP_API_KEY')
        
        # API endpoints
        self.endpoints = {
            'stackoverflow': 'https://api.stackexchange.com/2.3',
            'bls': 'https://api.bls.gov/publicAPI/v2',
            'github': 'https://api.github.com',
            'dice': 'https://marketplace-api.dice.com/v1',
            'coursera': 'https://api.coursera.org/api/courses.v1',
            'udemy': 'https://www.udemy.com/api-2.0',
            'hackernews': 'https://hacker-news.firebaseio.com/v0',
            'meetup': 'https://api.meetup.com/gql'
        }
        
        self.cached_data = {}

    async def _get_coursera_courses(self, role: str) -> Dict:
        """Get course recommendations from Coursera"""
        try:
            async with aiohttp.ClientSession() as session:
                headers = {'Authorization': f'Bearer {self.coursera_api_key}'}
                params = {
                    'q': role,
                    'fields': 'name,slug,workload,rating,specializations'
                }
                
                async with session.get(
                    f"{self.endpoints['coursera']}/search",
                    headers=headers,
                    params=params
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            'courses': data.get('elements', [])[:5],
                            'source': 'Coursera',
                            'last_updated': datetime.now().isoformat()
                        }
        except Exception as e:
            print(f"Error fetching Coursera data: {str(e)}")
            return self._get_fallback_coursera_data()

    def _get_fallback_coursera_data(self) -> Dict:
        """Provide fallback course data when API fails"""
        return {
            'courses': [
                {
                    'name': 'Python Programming Basics',
                    'provider': 'Coursera',
                    'rating': 4.5,
                    'duration': '6 weeks'
                }
            ],
            'source': 'Fallback Data',
            'last_updated': datetime.now().isoformat()
        }
