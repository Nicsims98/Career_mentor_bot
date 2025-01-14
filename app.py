from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:5000", "http://127.0.0.1:5000"]}})
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# create SQLAlchemy instance
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# database tables
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=True)
    work_type = db.Column(db.String(50), nullable=True)
    location = db.Column(db.String(100), nullable=True)
    job_preference = db.Column(db.String(100), nullable=True)
    skills = db.Column(db.Text, nullable=True)  # Store as comma-separated values
    interests = db.Column(db.Text, nullable=True)  # Store as comma-separated values
    education = db.Column(db.Text, nullable=True) # Store as comma-separated values
    work_experience = db.Column(db.Text, nullable=True) # Store as comma-separated values
    short_term_career_goals = db.Column(db.Text, nullable=True)
    long_term_career_goals = db.Column(db.Text, nullable=True)

class InternshipListings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    company_name = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200), nullable=True)
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    duration = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=True)
    requirements = db.Column(db.Text, nullable=True)
    compensation = db.Column(db.String(200), nullable=True)
    application_deadline = db.Column(db.Date, nullable=True)
    contact_email = db.Column(db.String(120), nullable=True)
    industry = db.Column(db.String(100), nullable=True)
    industry_type = db.Column(db.String(50), nullable=True)  # summer, part-time, full-time

class ChatLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(200), nullable=True)
    question = db.Column(db.Text, nullable=False)
    advice = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

class Recommendations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    courses = db.Column(db.Text, nullable=True)  # Store as comma-separated values or JSON
    companies = db.Column(db.Text, nullable=True)  # Store as comma-separated values or JSON
    career_paths = db.Column(db.Text, nullable=True)  # Store as comma-separated values or JSON

class Mentorship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    method_of_contact = db.Column(db.String(100), nullable=False)
    expertise = db.Column(db.Text, nullable=False)
    experience = db.Column(db.Text, nullable=False)
    availability = db.Column(db.Text, nullable=False)

@app.route('/')
def home():
    return "Career Mentor Bot"

@app.route('/userinput', methods=['POST'])
def add_user():
    try:
        data = request.get_json()
        print("Received data:", data)  # Debug log
        
        # Validate required fields
        if not data:
            return jsonify({"error": "No data received"}), 400
        if not data.get('email'):
            return jsonify({"error": "Email is required"}), 400
            
        # Check if user already exists
        existing_user = User.query.filter_by(email=data.get('email')).first()
        if existing_user:
            return jsonify({"error": "User with this email already exists"}), 409

        # Convert age to integer if it's provided
        age = data.get('age')
        if age and isinstance(age, str):
            try:
                age = int(age)
            except ValueError:
                return jsonify({"error": "Age must be a number"}), 400

        # Create new user
        new_user = User(
            name=data.get('name'),
            email=data.get('email'),
            age=age,
            location=data.get('location'),
            work_type=data.get('workType'),
            job_preference=data.get('jobPreference'),
            skills=data.get('skills'),
            interests=data.get('interests'),
            education=data.get('education'),
            work_experience=data.get('experience'),
            short_term_career_goals=data.get('shortTermGoals'),
            long_term_career_goals=data.get('longTermGoals')
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User Profile added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/get_users')
def get_users():
    try:
        users = User.query.all()
        return jsonify([{
            'name': user.name,
            'email': user.email,
            'age': user.age,
            'location': user.location,
            'workType': user.work_type,
            'jobPreference': user.job_preference,
            'skills': user.skills,
            'interests': user.interests,
            'education': user.education,
            'experience': user.work_experience,
            'shortTermGoals': user.short_term_career_goals,
            'longTermGoals': user.long_term_career_goals
        } for user in users])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
