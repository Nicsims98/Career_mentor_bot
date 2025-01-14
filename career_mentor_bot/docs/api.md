# Sage Career Mentor API Documentation

## Authentication
All endpoints require API key authentication:
```
Authorization: Bearer <your_api_key>
```

## Endpoints

### Career Guidance

#### Get Career Advice
`POST /api/sage/chat`

Request:
```json
{
    "message": "What skills do I need for AI development?",
    "type": "skill_advice",
    "context": {
        "current_skills": ["python", "mathematics"],
        "experience_level": "intermediate"
    }
}
```

Response:
```json
{
    "response": "...",
    "recommendations": [...],
    "metrics": {...}
}
```

#### Get Course Recommendations
`POST /api/sage/recommend-courses`

Request:
```json
{
    "skills": ["python", "javascript"],
    "career_goal": "Full Stack Developer",
    "available_hours": 10,
    "learning_pace": "moderate"
}
```

Response:
```json
{
    "courses": [...],
    "learning_path": {...},
    "time_estimate": "..."
}
```

### Market Insights

#### Update LinkedIn Data
`POST /api/sage/linkedin/jobs`

Request:
```json
{
    "jobs": [
        {
            "id": "job123",
            "title": "Senior Developer",
            "company": "Tech Corp",
            "location": "Remote",
            "description": "...",
            "salary": "$120K-$150K"
        }
    ]
}
```

Response:
```json
{
    "success": true,
    "metrics": {
        "processed_jobs": 95,
        "failed_jobs": 5,
        "processing_time": 1.23
    }
}
```

### Visualization

#### Get Market Trends
`GET /api/sage/visualizations/market-trends`

Parameters:
- role (string): Job role
- region (string): Geographic region
- timeframe (string): Data timeframe

Response:
```json
{
    "visualization_data": {...},
    "insights": {...},
    "metadata": {...}
}
```

## Error Handling

### Error Codes
- E001: Invalid input
- E002: Rate limit exceeded
- E003: Authentication error
- E004: API error
- E005: Database error

### Error Response Format
```json
{
    "error": "Error message",
    "code": "ERROR_CODE",
    "details": {...}
}
```

## Rate Limits
- 100 requests per minute per IP
- 1000 requests per day per API key

## Data Schemas

### Job Data Schema
```json
{
    "id": "string",
    "title": "string",
    "company": "string",
    "location": "string",
    "description": "string",
    "salary": "string",
    "required_skills": ["string"],
    "experience_level": "string"
}
```

### Metrics Schema
```json
{
    "total_jobs": "number",
    "processed_jobs": "number",
    "failed_jobs": "number",
    "processing_time": "number",
    "status": "string",
    "errors": ["string"]
}
```

## Best Practices

1. Error Handling
```python
try:
    response = await api.get_career_advice(message)
except ApiError as e:
    handle_error(e)
```

2. Rate Limiting
```python
if rate_limiter.can_proceed(api_key):
    process_request()
else:
    return rate_limit_exceeded_error()
```

3. Data Validation
```python
def validate_job_data(job):
    if not all(required_fields):
        raise ValidationError()
```
