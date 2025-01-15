"""
LinkedIn job data integration handler with validation and error handling
"""

from typing import Dict, List, Any, Optional
import asyncio
from datetime import datetime
from dataclasses import dataclass
import logging
from enum import Enum

class JobDataError(Exception):
    """Custom exception for job data processing errors"""
    pass

class DataValidationError(Exception):
    """Custom exception for data validation errors"""
    pass

class ProcessingStatus(Enum):
    SUCCESS = "success"
    PARTIAL = "partial"
    FAILED = "failed"

@dataclass
class ProcessingMetrics:
    total_jobs: int
    processed_jobs: int
    failed_jobs: int
    processing_time: float
    status: ProcessingStatus
    errors: List[str]

class LinkedInDataHandler:
    def __init__(self):
        self.cache_duration = 3600  # 1 hour cache
        self.cached_data = {}
        self.logger = logging.getLogger('linkedin.handler')
        
        # Required fields for validation
        self.required_fields = {
            'id': str,
            'title': str,
            'company': str,
            'location': str,
            'description': str
        }

    def validate_job_data(self, job: Dict) -> List[str]:
        """Validate individual job data"""
        errors = []
        
        # Check required fields
        for field, field_type in self.required_fields.items():
            if field not in job:
                errors.append(f"Missing required field: {field}")
            elif not isinstance(job.get(field), field_type):
                errors.append(f"Invalid type for {field}: expected {field_type}")
        
        # Validate data formats
        if 'salary' in job and not self._is_valid_salary_format(job['salary']):
            errors.append("Invalid salary format")
            
        if 'posted_date' in job and not self._is_valid_date(job['posted_date']):
            errors.append("Invalid date format")
            
        return errors

    async def process_scraped_data(self, job_data: List[Dict[str, Any]]) -> Dict:
        """Process incoming scraped LinkedIn data with validation and metrics"""
        start_time = datetime.now()
        metrics = ProcessingMetrics(
            total_jobs=len(job_data),
            processed_jobs=0,
            failed_jobs=0,
            processing_time=0,
            status=ProcessingStatus.SUCCESS,
            errors=[]
        )
        
        try:
            # Validate all jobs
            valid_jobs = []
            for job in job_data:
                validation_errors = self.validate_job_data(job)
                if validation_errors:
                    metrics.failed_jobs += 1
                    metrics.errors.extend(validation_errors)
                    continue
                    
                valid_jobs.append(job)
            
            metrics.processed_jobs = len(valid_jobs)
            
            # Process valid jobs
            processed_data = {
                'jobs': self._process_jobs(valid_jobs),
                'skills': self._extract_skills(valid_jobs),
                'companies': self._analyze_companies(valid_jobs),
                'salary_ranges': self._analyze_salaries(valid_jobs),
                'last_updated': datetime.now().isoformat()
            }
            
            # Update cache if we have valid data
            if processed_data['jobs']:
                self.cached_data = processed_data
            
            # Determine processing status
            if metrics.failed_jobs == metrics.total_jobs:
                metrics.status = ProcessingStatus.FAILED
            elif metrics.failed_jobs > 0:
                metrics.status = ProcessingStatus.PARTIAL
            
            # Calculate processing time
            metrics.processing_time = (datetime.now() - start_time).total_seconds()
            
            # Log metrics
            self._log_processing_metrics(metrics)
            
            return {
                'data': processed_data,
                'metrics': {
                    'total_jobs': metrics.total_jobs,
                    'processed_jobs': metrics.processed_jobs,
                    'failed_jobs': metrics.failed_jobs,
                    'processing_time': metrics.processing_time,
                    'status': metrics.status.value,
                    'errors': metrics.errors
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error processing LinkedIn data: {str(e)}")
            raise JobDataError(f"Failed to process job data: {str(e)}")

    def _log_processing_metrics(self, metrics: ProcessingMetrics):
        """Log processing metrics"""
        self.logger.info(
            f"LinkedIn data processing completed:\n"
            f"Status: {metrics.status.value}\n"
            f"Total Jobs: {metrics.total_jobs}\n"
            f"Processed: {metrics.processed_jobs}\n"
            f"Failed: {metrics.failed_jobs}\n"
            f"Processing Time: {metrics.processing_time:.2f}s"
        )
        
        if metrics.errors:
            self.logger.warning(
                "Processing errors occurred:\n" +
                "\n".join(metrics.errors)
            )

    def _is_valid_salary_format(self, salary: str) -> bool:
        """Validate salary format"""
        import re
        # Match formats like "$100K-$150K" or "$100,000-$150,000"
        pattern = r'^\$?\d{1,3}(?:,\d{3})*(?:K)?(?:-\$?\d{1,3}(?:,\d{3})*(?:K)?)?$'
        return bool(re.match(pattern, salary))

    def _is_valid_date(self, date_str: str) -> bool:
        """Validate date format"""
        try:
            datetime.fromisoformat(date_str)
            return True
        except ValueError:
            return False
