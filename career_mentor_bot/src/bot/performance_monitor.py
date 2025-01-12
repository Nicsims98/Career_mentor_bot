"""
AI Performance Monitoring for Sage
"""

import time
from datetime import datetime
from typing import Dict, Any, Optional
import logging
from dataclasses import dataclass

@dataclass
class ResponseMetrics:
    response_time: float
    token_count: int
    prompt_tokens: int
    completion_tokens: int
    model: str
    total_cost: float

class PerformanceMonitor:
    def __init__(self):
        self.logger = logging.getLogger('sage.ai.performance')
        self.logger.setLevel(logging.INFO)
        
        # Add file handler
        fh = logging.FileHandler('logs/ai_performance.log')
        fh.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        self.logger.addHandler(fh)
        
        # Token costs per model
        self.token_costs = {
            'gpt-4': {
                'prompt': 0.03,
                'completion': 0.06
            },
            'gpt-3.5-turbo': {
                'prompt': 0.002,
                'completion': 0.002
            }
        }
    
    def start_request(self) -> float:
        """Start timing a request"""
        return time.time()
    
    def calculate_metrics(
        self,
        start_time: float,
        completion: Any,
        model: str
    ) -> ResponseMetrics:
        """Calculate performance metrics for a response"""
        end_time = time.time()
        response_time = end_time - start_time
        
        # Calculate token counts and costs
        prompt_tokens = completion.usage.prompt_tokens
        completion_tokens = completion.usage.completion_tokens
        
        # Calculate cost
        model_costs = self.token_costs.get(model, self.token_costs['gpt-3.5-turbo'])
        total_cost = (
            (prompt_tokens * model_costs['prompt'] / 1000) +
            (completion_tokens * model_costs['completion'] / 1000)
        )
        
        return ResponseMetrics(
            response_time=response_time,
            token_count=prompt_tokens + completion_tokens,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            model=model,
            total_cost=total_cost
        )
    
    def log_metrics(self, metrics: ResponseMetrics, request_type: str):
        """Log performance metrics"""
        self.logger.info(
            f"Request Type: {request_type} | "
            f"Model: {metrics.model} | "
            f"Response Time: {metrics.response_time:.2f}s | "
            f"Tokens: {metrics.token_count} | "
            f"Cost: ${metrics.total_cost:.4f}"
        )
