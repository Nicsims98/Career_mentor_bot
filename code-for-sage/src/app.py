"""
Main Flask application for Sage career mentor bot
"""

from flask import Flask, jsonify, request, render_template
from src.database import db, init_db
from flask_cors import CORS
from src.api.routes import sage_bp
from src.config import get_config
from src.models.user import User  # Import models from their own files
from src.models.chat_history import ChatHistory
import logging
import os
from src.bot.integrations.linkedin_handler import LinkedInDataHandler
from src.bot.performance_monitor import PerformanceMonitor
from src.bot.market_insights import MarketInsights
import openai

openai_api_key = os.getenv('OPENAI_API_KEY')

class SageApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.setup_app()
        
    def setup_app(self):
        # Load configuration
        env = os.getenv('FLASK_ENV', 'development')
        self.app.config.from_object(get_config(env))
        
        # Configure database
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        # Initialize database
        init_db(self.app)
        
        # Initialize services
        self.linkedin_handler = LinkedInDataHandler()
        self.performance_monitor = PerformanceMonitor()
        self.market_insights = MarketInsights()
        
        # Configure CORS
        CORS(self.app, resources={
            r"/*": {  # Allow CORS for all routes
                "origins": ["http://localhost:5173", "http://localhost:5000", "http://localhost:5001"],
                "methods": ["GET", "POST", "OPTIONS"],
                "allow_headers": ["Content-Type", "Authorization", "X-Requested-With", "Accept", "Origin", "Access-Control-Request-Method", "Access-Control-Request-Headers"]
            }
        })
        
        # Register blueprints
        self.app.register_blueprint(sage_bp, url_prefix='/api/sage')
        
        # Register additional routes
        self.register_routes()
        
    def register_routes(self):
        @self.app.route('/health', methods=['GET'])
        def health_check():
            return {
                'status': 'healthy',
                'message': 'Sage is ready to help!',
                'version': '1.0.0',
                'features': [
                    'Course Recommendations',
                    'Time Analysis',
                    'Schedule Planning',
                    'Learning Path Generation'
                ],
                'dependencies': {
                    'openai': 'active',
                    'database': 'active',
                    'linkedin': 'active'
                }
            }

        @self.app.route('/')
        def home():
            return "Career Mentor Bot"

        @self.app.route('/userinput', methods=['POST'])
        def add_user():
            try:
                data = request.get_json()
                logging.info(f"Received user input data: {data}")  # Add logging
                
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
                
                # Add to database within a try block
                try:
                    db.session.add(new_user)
                    db.session.commit()
                    logging.info(f"Successfully added user: {new_user.email}")  # Add logging
                    return jsonify({"message": "User Profile added successfully"}), 201
                except Exception as db_error:
                    db.session.rollback()
                    logging.error(f"Database error: {str(db_error)}")  # Add logging
                    return jsonify({"error": "Database error occurred"}), 500
                    
            except Exception as e:
                logging.error(f"Error in add_user: {str(e)}")  # Add logging
                return jsonify({"error": str(e)}), 400

        @self.app.route('/get_users', methods=['GET'])
        def get_users():
            try:
                users = User.query.all()
                logging.info(f"Retrieved {len(users)} users")  # Add logging
                
                if not users:
                    return jsonify([]), 200  # Return empty list if no users
                    
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
                logging.error(f"Error in get_users: {str(e)}")  # Add logging
                return jsonify({"error": str(e)}), 500

def create_app():
    sage_app = SageApp()
    return sage_app.app

if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    app = create_app()
    with app.app_context():
        db.create_all()  # Create tables within app context
    app.run(debug=True, port=5000)
