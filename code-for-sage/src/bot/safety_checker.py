"""
AI Safety and Content Filtering for Sage
"""

from typing import Dict, List, Tuple
import re
from dataclasses import dataclass
from datetime import datetime, timedelta
import logging

@dataclass
class SafetyCheck:
    is_safe: bool
    issues: List[str]
    filtered_content: str

class SafetyChecker:
    def __init__(self):
        self.logger = logging.getLogger('sage.ai.safety')
        self.request_history = {}
        self.rate_limits = {
            'user': 50,  # requests per hour
            'ip': 100    # requests per hour
        }
        
        # Basic content filtering patterns
        self.filtered_patterns = [
            (r'\b(hate|violent|explicit)\b', '[filtered]'),
            (r'(https?://\S+)', '[no-urls]'),
            (r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '[no-phone-numbers]')
        ]
    
    def check_rate_limit(self, user_id: str, ip: str) -> Tuple[bool, str]:
        """Check if request is within rate limits"""
        current_time = datetime.now()
        hour_ago = current_time - timedelta(hours=1)
        
        # Clean old entries
        self.request_history = {
            k: v for k, v in self.request_history.items()
            if v['timestamp'] > hour_ago
        }
        
        # Check user limit
        user_requests = len([
            r for r in self.request_history.values()
            if r['user_id'] == user_id and r['timestamp'] > hour_ago
        ])
        
        if user_requests >= self.rate_limits['user']:
            return False, "User rate limit exceeded"
            
        # Check IP limit
        ip_requests = len([
            r for r in self.request_history.values()
            if r['ip'] == ip and r['timestamp'] > hour_ago
        ])
        
        if ip_requests >= self.rate_limits['ip']:
            return False, "IP rate limit exceeded"
            
        return True, "OK"
    
    def filter_content(self, content: str) -> SafetyCheck:
        """Filter and check content for safety"""
        issues = []
        filtered_content = content
        
        # Apply content filters
        for pattern, replacement in self.filtered_patterns:
            if re.search(pattern, filtered_content):
                issues.append(f"Found potentially unsafe content matching {pattern}")
                filtered_content = re.sub(pattern, replacement, filtered_content)
        
        # Check content length
        if len(content) > 4000:
            issues.append("Content exceeds maximum length")
            filtered_content = filtered_content[:4000] + "..."
        
        return SafetyCheck(
            is_safe=len(issues) == 0,
            issues=issues,
            filtered_content=filtered_content
        )
    
    def log_request(self, user_id: str, ip: str, request_type: str):
        """Log a request for rate limiting"""
        request_id = f"{user_id}_{datetime.now().timestamp()}"
        self.request_history[request_id] = {
            'user_id': user_id,
            'ip': ip,
            'timestamp': datetime.now(),
            'request_type': request_type
        }
