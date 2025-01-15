"""
Flask routes for Sage - handles all chat and course/job recommendation interactions
"""

from flask import Blueprint, request, jsonify, current_app
from src.bot.integrations.linkedin_handler import JobDataError, DataValidationError
from src.bot.openai_handler import SageAI
from src.bot.course_recommender import CourseRecommender, LearningPace, JobMatchLevel
from src.bot.integrations.linkedin_handler import LinkedInDataHandler
from src.config import Config
from src.bot.safety_checker import SafetyChecker
from src.models.chat_history import ChatHistory
from flask import current_app
from src.database import db

# Initialize services
sage_ai = SageAI()
safety_checker = SafetyChecker()

# Create blueprint for all Sage routes
sage_bp = Blueprint('sage', __name__)

# Initialize services
sage_ai = SageAI()
course_recommender = CourseRecommender()
linkedin_handler = LinkedInDataHandler()

@sage_bp.route('/chat', methods=['POST'])
async def chat():
    """Main chat endpoint"""
    try:
        current_app.logger.info("Received chat request")
        data = request.json
        current_app.logger.info(f"Request data: {data}")
        
        message = data.get('message')
        
        if not message:
            return jsonify({
                'error': 'No message provided'
            }), 400
            
        # Get user IP and generate a temporary user ID if not authenticated
        ip = request.remote_addr
        user_id = request.headers.get('X-User-ID', f'temp_{ip}')
        
        # Check rate limits
        is_allowed, limit_message = safety_checker.check_rate_limit(user_id, ip)
        if not is_allowed:
            return jsonify({
                'error': limit_message,
                'code': Config.ERROR_CODES['RATE_LIMIT']
            }), 429
            
        # Log the request
        safety_checker.log_request(user_id, ip, 'chat')
        
        # Get AI response
        current_app.logger.info("Calling OpenAI API...")
        try:
            response = sage_ai.chat(message)
            current_app.logger.info("Got response from OpenAI")
        except Exception as e:
            current_app.logger.error(f"OpenAI API error: {str(e)}")
            raise
        
        # Store in chat history
        chat_history = ChatHistory(
            user_id=user_id,
            message=message,
            response=response,
            prompt_type='general'
        )
        db.session.add(chat_history)
        db.session.commit()
        
        return jsonify({
            'response': response
        })
        
    except Exception as e:
        current_app.logger.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({
            'error': str(e),
            'code': Config.ERROR_CODES['API_ERROR'],
            'message': Config.ERROR_MESSAGES[Config.ERROR_CODES['API_ERROR']]
        }), 500
