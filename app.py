from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)
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
    skills = db.Column(db.Text, nullable=True)  # Store as comma-separated values
    interests = db.Column(db.Text, nullable=True)  # Store as comma-separated values
    education = db.Column(db.Text, nullable=True) # Store as comma-separated values
    work_experience = db.Column(db.Text, nullable=True) # Store as comma-separated values
    short_term_career_goals = db.Column(db.Text, nullable=True)
    long_term_career_goals = db.Column(db.Text, nullable=True)

@app.route('/')
def home():
    return "Career Mentor Bot"

@app.route('/add_user', methods=['POST'])
def add_user():
    try:
        data = request.form
        new_user = User(
            name=data.get('name'),
            email=data.get('email'),
            age=data.get('age'),
            work_type=data.get('work_type'),
            location=data.get('location'),
            skills=data.get('skills'),
            interests=data.get('interests'),
            education=data.get('education'),
            work_experience=data.get('work_experience'),
            short_term_career_goals=data.get('short_term_career_goals'),
            long_term_career_goals=data.get('long_term_career_goals')
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User Profile added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/get_users')
def get_users():
    users = User.query.all()
    return jsonify([{
        'name': user.name,
        'email': user.email,
        'age': user.age,
        'work_type': user.work_type,
        'location': user.location,
        'skills': user.skills.split(',') if user.skills else [],
        'interests': user.interests.split(',') if user.interests else [],
        'education': user.education.split(',') if user.education else [],
        'work_experience': user.work_experience.split(',') if user.work_experience else [],
        'short_term_career_goals': user.short_term_career_goals.split(',') if user.short_term_career_goals else [],
        'long_term_career_goals': user.long_term_career_goals.split(',') if user.long_term_career_goals else []
    } for user in users])


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
