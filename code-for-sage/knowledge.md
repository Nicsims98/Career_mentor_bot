# Sage Career Mentor Bot Knowledge Base

## Project Overview
AI-powered career guidance and learning path recommendation system.

## Key Guidelines
- Always add logging for monitoring and debugging
- Use type hints for better code maintainability
- Follow PEP 8 style guidelines
- Keep security and rate limiting in mind for all endpoints
- Use absolute imports (e.g., from src.bot.something import X) not relative imports

## Development Setup
1. Create and activate virtual environment
2. Install dependencies: `pip install -r requirements.txt`
3. Set up `.env` file with required API keys
4. Run tests: `pytest`

## Server Configuration
- Backend runs on port 5000 (Flask backend in code-for-sage/src/app.py)
- Frontend runs on port 5173 (React frontend served by Vite)
- Configure CORS in app.py to allow frontend origin

## CORS Configuration
- Keep OPTIONS method in CORS configuration
- Browser sends OPTIONS request before POST (CORS preflight)
- Required for cross-origin requests to work
- Never remove OPTIONS from CORS methods as it breaks cross-origin requests
- Frontend must use exact matching port when making requests to backend
- Backend runs on port 5000 (Flask backend in code-for-sage/src/app.py)
- Frontend runs on port 5173 (React frontend served by Vite)
- API endpoints must match exactly between frontend and backend
- CORS headers must include full set: Content-Type, Authorization, X-Requested-With, Accept, Origin, Access-Control-Request-Method, Access-Control-Request-Headers

## Important URLs
- OpenAI API docs: https://platform.openai.com/docs/api-reference
- OpenAI API keys: https://platform.openai.com/api-keys

## Environment Variables
Required environment variables in `.env`:
- OPENAI_API_KEY: Your OpenAI API key (starts with "sk-...")
  - Required for chat functionality
  - Free tier includes $5 credit
  - Rate limits apply
  - Keep secure, never commit to repo
- FLASK_ENV: development/production

## Testing Chat Functionality
1. Ensure OpenAI API key is configured
2. Start Flask backend (port 5001)
3. Start Vite frontend (port 5174)
4. Send test message through interface

## API Testing with Postman
Test the chat endpoint directly:
- URL: http://localhost:5001/api/sage/chat
- Method: POST
- Headers: Content-Type: application/json
- Body (raw JSON):
```json
{
    "message": "Hello",
    "type": "general"
}
```
