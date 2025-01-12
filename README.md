# VSNE Career Mentor Bot

**VSNE** is a career mentor chatbot designed to provide personalized career guidance. Using advanced AI and web scraping techniques, it offers tailored recommendations for career paths, courses, companies, and internship opportunities.

This is for the 2025 nosu hackathon! A team of four baddies in tech made this project come to life!
---

## Features

### Core Functionalities
1. **Interactive Q&A**: Engage in conversations to understand the user's background, interests, experience(if any) and skills.

2. **Personalized Roadmap**:
   - Suggests career paths.
   - Recommends online courses and learning resources.

3. **Internship Finder**: Scrape and display relevant internship opportunities.

4. **Chatbot**: For Q&A interactions.
---

## User Flow
1. **Welcome Screen**
- Introduce the bot’s purpose and what users can expect.

2. **Input Form**
- Users fill out their details: Skills, interests, education, etc.

3. **Display Roadmap**
- Provide:
  - Suggested roles with descriptions.
  - Links to relevant courses and learning resources.

4. **Chatbot Interaction**
- Allow users to ask follow-up questions about roles, skills, or industries.

---

## Tech Stack

### **Frontend**
- **React**: For creating a sleek and interactive chat interface.
- **Axios**: For API calls.

### **Backend**
- **Flask**: To handle API requests and integrate backend logic.
- **SQL**: To manage user data, chat logs, and recommendation history.

### **AI Component**
- **OpenAI API**: Powers conversational logic and personalized recommendations.

### **Web Scraping**
- **Python**: To fetch internship opportunities and LinkedIn profiles.

### **AI/ML**
- Model: OpenAI GPT API for:
- Role and resource recommendations.
- Career Q&A chatbot.

### **Hosting**
- Frontend: Netlify or Vercel for React app.
- Backend: Render or Heroku for Flask/Node.js API.

---

## Project Roles

### Team Members
- **Nic**: AI Component (Flask, OpenAI API).
- **Ewa**: Frontend Development (React).
- **Sab**: Backend Development (Flask, SQL).
- **Vee**: Web Scraping (Internships and LinkedIn profiles).

---

## Future Enhancements

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
