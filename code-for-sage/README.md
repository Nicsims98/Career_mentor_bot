# Sage Career Mentor Bot

## Prerequisites
- Python 3.13 or higher
- Node.js and npm
- Virtual environment tool (venv)

## Backend Setup (Flask)

1. Create and activate virtual environment:
```bash
cd code-for-sage
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
pip install "flask[async]"
```

3. Set up environment variables:
- Create a `.env` file in code-for-sage directory
- Add your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
FLASK_ENV=development
```

4. Initialize database:
```bash
flask db init
flask db migrate
flask db upgrade
```

5. Start Flask server:
```bash
FLASK_APP=src/app.py FLASK_ENV=development FLASK_DEBUG=1 flask run --port 5001
```
Backend will run on http://127.0.0.1:5001

## Frontend Setup (React/Vite)

1. Install dependencies:
```bash
cd src  # Navigate to frontend directory
npm install
```

2. Start Vite development server:
```bash
npm run dev
```
Frontend will run on http://localhost:5173

## Common Issues

### Backend
- If port 5000 is in use (common on macOS):
  - Disable AirPlay Receiver in System Preferences -> General -> AirDrop & Handoff
  - Or use different port: `flask run --port 5001`
- If pip not found: Activate virtual environment
- If modules missing: Run pip install from code-for-sage directory

### Frontend
- If npm modules are missing: Run `npm install` in src directory
- If port 5173 is in use: Vite will automatically try next available port

## API Testing
Test the chat endpoint:
```bash
curl -X POST http://localhost:5001/api/sage/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}'
```

## Development Notes
- Backend API runs on port 5001 by default
- Frontend development server runs on port 5173
- Make sure both servers are running for full functionality
- Check console logs for any errors
- Ensure CORS settings match your port configuration