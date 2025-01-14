# VSNE Career Mentor Bot 🚀

Welcome to the **VSNE Career Mentor Bot** repository! This project was built during the NoSu AI Hackathon by a team of four passionate developers to create an AI-powered career mentor. The bot is designed to guide users toward their ideal career paths, offering tailored roadmaps and resources. 🌟

This is for the 2025 nosu hackathon! A team of four baddies in tech made this project come to life!
## Tracks we’re going for 
-	Most Technically impressive - Modal
-	Beginner track
-	Best personal project (CodeBuff)
-	Statsig Grand Prize, Best overall project
-	Magic Loops
-	Generative UI/UX 
-	Nethenoob spinning cat
-	Bill Zhang Conversational AI Prize
-	Education and AI
  
## Features ✨
- **Personalized Career Roadmap** 🗺️: A step-by-step guide to achieving your dream career, with actionable steps and course links.
- **Interactive Chat with Sage** 💬: Get advice and insights from Sage, our AI-powered chat assistant.
- **User-Friendly Interface** 🎨: A clean and modern design for seamless navigation.
- **Dark Mode Support** 🌙: Switch between light and dark themes to suit your preference.

## Pages 📄
### 1. Home Page 🏠
- Overview of the bot and its capabilities.
- Steps on how to use the platform.
- Call-to-action buttons to get started or learn more.

### 2. User-Input Page 📝
- Collects user information like name, interests, current skills, and career goals.
- Provides a seamless way to start the personalized experience.

### 3. Roadmap Page 🛤️
- Displays the most recommended career path based on user input.
- Features a dynamic roadmap with 10 color-coded pointers for actionable steps.
- Each step includes an explanation and a link to relevant courses or resources.
- Includes interactive guidance from Sage to help users along the way.

## Technology Stack 🛠️
- **Frontend:** React, Vanilla CSS
- **Backend:** Flask, SQLAlchemy
- **AI/ML:** OpenAI API for conversational intelligence
- **Database:** SQLite
- **Additional Tools:** HTML, CSS, JavaScript

### **Hosting** ▶️
- Frontend: Netlify or Vercel for React app.
- Backend: Render or Heroku for Flask/Node.js API.

## Future Improvements 🚧
1. **Advanced AI Capabilities**:
   - More in-depth career path analysis.
   - Real-time user feedback integration.
   - Career comparison tool (e.g., compare two roles).
2. **Mentorship Matching**:
   - Mentor matching based on career goals.
3. **Basic Resume Analysis** 
   - Upload a resume to receive:
   - Skill gaps for target roles: Basic improvement tips (e.g., adding action verbs or quantifying achievements).
   - Save Progress/History: Enable users to save their profile and revisit recommendations or chat history.
4. **Internship Finder**
   - Find potential internships for user to apply to.
5. Incorporate gamification elements for user engagement.

## Team 👩‍💻👨‍💻
- **Nic:** AI integration and Flask API development.
- **Ewa:** Frontend development and design.
- **Sab:** Backend development and database management.
- **Vee:** Web scraping for internships and LinkedIn profiles.

---

Thank you for checking out the VSNE Career Mentor Bot! 🌈 If you have any questions or feedback, please feel free to reach out. Let’s help you take the next step in your career journey! 💼✨
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
