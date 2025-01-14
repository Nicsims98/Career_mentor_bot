"""
Utility functions for time calculations and schedule management
"""

from datetime import datetime, timedelta
from typing import Dict, List

def calculate_study_blocks(
    total_hours: int,
    min_block_size: int = 30,
    max_block_size: int = 120
) -> List[int]:
    """Calculate optimal study block sizes"""
    if total_hours < 1:
        return [30]  # Minimum 30-minute blocks
        
    hours_in_minutes = total_hours * 60
    optimal_block_size = min(max(min_block_size, hours_in_minutes // 3), max_block_size)
    
    return [optimal_block_size] * (hours_in_minutes // optimal_block_size)

def generate_weekly_schedule(
    available_hours: int,
    preferred_times: List[str] = None
) -> Dict:
    """Generate a weekly schedule template"""
    if not preferred_times:
        preferred_times = ['morning', 'evening']
        
    blocks = calculate_study_blocks(available_hours)
    
    schedule = {
        'recommended_blocks': blocks,
        'daily_distribution': _distribute_hours(available_hours, 7),
        'weekly_structure': _create_weekly_template(blocks, preferred_times)
    }
    
    return schedule

def _distribute_hours(total_hours: int, days: int) -> List[float]:
    """Distribute hours across days"""
    base_hours = total_hours / days
    return [round(base_hours, 1)] * days

def _create_weekly_template(
    blocks: List[int],
    preferred_times: List[str]
) -> Dict:
    """Create a weekly schedule template"""
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    schedule = {}
    
    for day in days:
        schedule[day] = {
            'recommended_blocks': len(blocks) // 7 or 1,
            'preferred_times': preferred_times,
            'flexibility': 'Adjust based on daily energy levels'
        }
    
    return schedule

def calculate_job_readiness_date(weeks_needed: int) -> str:
    """
    Calculate estimated date of job readiness
    """
    target_date = datetime.now() + timedelta(weeks=weeks_needed)
    return target_date.strftime('%Y-%m-%d')