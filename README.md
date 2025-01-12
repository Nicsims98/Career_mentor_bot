# Sage Career Mentor Bot - AI Component

AI-powered career guidance and learning path recommendation system.

## Setup

1. Clone the repository
2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your actual values
```

5. Run the development server:
```bash
flask run
```

## API Endpoints

### Chat Endpoint
POST `/api/sage/chat`
```json
{
    "message": "What career path should I take?",
    "type": "career_path"
}
```

### Course Recommendations
POST `/api/sage/recommend-courses`
```json
{
    "skills": ["python", "javascript"],
    "career_goal": "Full Stack Developer",
    "available_hours": 10,
    "learning_pace": "moderate"
}
```

## Development

### Running Tests
```bash
pytest
```

### Code Style
```bash
flake8 src tests
