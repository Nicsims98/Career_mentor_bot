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
1. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```
2. Install minimum required dependencies:
```bash
pip install flask flask-cors flask-sqlalchemy flask-migrate python-dotenv openai aiohttp
pip install "flask[async]"  # Required for async route handlers
```
3. Set up `.env` file with required API keys
4. Run the Flask app:
```bash
cd code-for-sage
FLASK_APP=src/app.py FLASK_ENV=development FLASK_DEBUG=1 flask run
```

## Running the Application
1. Always run from code-for-sage directory
2. Ensure virtual environment is activated:
   ```bash
   source venv/bin/activate
   ```
3. Start server:
   ```bash
   FLASK_APP=src/app.py FLASK_ENV=development FLASK_DEBUG=1 flask run
   ```
4. Server runs on http://127.0.0.1:5000
5. Use Ctrl+C to stop server
6. Debug mode shows detailed errors and enables auto-reload

Common Issues:
- If pip not found: Activate virtual environment
- If modules missing: Run pip install from code-for-sage directory
- If port 5000 in use: 
  - On macOS: Disable AirPlay Receiver in System Preferences -> General -> AirDrop & Handoff
  - Or use different port: `flask run --port 5001`
  - Frontend must update API_URL to match new port
  - Update CORS origins if using different port
1. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```
2. Install dependencies:
```bash
pip install -r requirements.txt
pip install "flask[async]"  # Required for async route handlers
```
3. Set up `.env` file with required API keys
4. Run the Flask app:
```bash
cd code-for-sage
FLASK_APP=src/app.py FLASK_ENV=development FLASK_DEBUG=1 flask run
```

## Running the Application
1. Always run from code-for-sage directory
2. Ensure virtual environment is activated:
   ```bash
   source venv/bin/activate
   ```
3. Start server:
   ```bash
   FLASK_APP=src/app.py FLASK_ENV=development FLASK_DEBUG=1 flask run
   ```
4. Server runs on http://127.0.0.1:5000
5. Use Ctrl+C to stop server
6. Debug mode shows detailed errors and enables auto-reload

Common Issues:
- If pip not found: Activate virtual environment
- If modules missing: Run pip install from code-for-sage directory
- If port 5000 in use: 
  - On macOS: Disable AirPlay Receiver in System Preferences -> General -> AirDrop & Handoff
  - Or use different port: `flask run --port 5001`
  - Frontend must update API_URL to match new port
  - Update CORS origins if using different port
5. Run tests: `pytest`

## Database Configuration
- Initialize SQLAlchemy in separate database.py module to avoid circular imports
- Use init_app pattern for SQLAlchemy setup
- Access db through current_app.db or import from database module
- Database operations should be within app context
- Never import db instance from app.py to avoid circular dependencies
- Always add session.rollback() in error handlers when database operations fail
- Keep model definitions in separate files, not in app.py
- Create database tables within app context using db.create_all()
- When setting up SQLAlchemy relationships:
  - Import related models explicitly
  - Define both sides of relationship (back_populates)
  - Define relationships after model attributes
  - Keep consistent table names in ForeignKey references

## Error Handling Best Practices
- Always wrap database operations in try-except blocks
- Add session.rollback() in database error handlers
- Log both successful operations and errors
- Return appropriate HTTP status codes (201 for creation, 409 for conflicts)
- Return empty lists instead of null for no results
- Include specific error messages in responses
- Initialize SQLAlchemy in separate database.py module to avoid circular imports
- Use init_app pattern for SQLAlchemy setup
- Access db through current_app.db or import from database module
- Database operations should be within app context
- Never import db instance from app.py to avoid circular dependencies
- Always add session.rollback() in error handlers when database operations fail
- Keep model definitions in separate files, not in app.py
- Create database tables within app context using db.create_all()
- When setting up SQLAlchemy relationships:
  - Import related models explicitly
  - Define both sides of relationship (back_populates)
  - Define relationships after model attributes
  - Keep consistent table names in ForeignKey references

## Server Configuration
- Development:
  - Backend runs on port 5000 (Flask backend in code-for-sage/src/app.py)
  - Frontend runs on port 5173 (React frontend served by Vite)
  - Configure CORS in app.py to allow frontend origin

## Deployment Configuration
- Backend URL: Find in Vercel dashboard under project's "Domains" section
- Environment Variables:
  - Set in Vercel dashboard (Settings > Environment Variables)
  - Required: OPENAI_API_KEY, VITE_API_URL
  - VITE_API_URL should be your Vercel backend domain + "/api/sage/chat"
  - For Vercel deployment: Set in Vercel dashboard (Settings > Environment Variables)
  - For other deployments: Set in platform's environment configuration
  - Default to gpt-3.5-turbo model unless GPT-4 access confirmed
  - Test API key access before deploying
  - Monitor API usage at platform.openai.com/account/usage
  - Set up billing at platform.openai.com/account/billing
  - Free tier credits expire after 3 months
  - Handle quota errors by directing users to billing page

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
  - For Vercel deployment: Set in Vercel dashboard (Settings > Environment Variables)
  - For other deployments: Set in platform's environment configuration
  - Default to gpt-3.5-turbo model unless GPT-4 access confirmed
  - Test API key access before deploying
  - Monitor API usage at platform.openai.com/account/usage
  - Set up billing at platform.openai.com/account/billing
  - Free tier credits expire after 3 months
  - Handle quota errors by directing users to billing page
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
