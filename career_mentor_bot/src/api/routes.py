"""
Flask routes for Sage - handles all chat and course/job recommendation interactions
"""

from flask import Blueprint, request, jsonify, current_app
from bot.integrations.linkedin_handler import JobDataError, DataValidationError
from bot.openai_handler import SageAI
from bot.course_recommender import CourseRecommender, LearningPace, JobMatchLevel
from bot.integrations.linkedin_handler import LinkedInDataHandler
from config import Config

# Create blueprint for all Sage routes
sage_bp = Blueprint('sage', __name__)

# Initialize services
sage_ai = SageAI()
course_recommender = CourseRecommender()
linkedin_handler = LinkedInDataHandler()



# LinkedIn integration endpoint
@sage_bp.route('/linkedin/jobs', methods=['POST'])
async def update_linkedin_jobs():
    """Endpoint for LinkedIn scraper to send job data"""
    try:
        # Validate request
        if not request.is_json:
            return jsonify({
                'error': 'Content-Type must be application/json',
                'code': 'INVALID_CONTENT_TYPE'
            }), 400

        job_data = request.json.get('jobs')
        if not job_data:
            return jsonify({
                'error': 'No job data provided',
                'code': 'MISSING_DATA'
            }), 400
        
        if not isinstance(job_data, list):
            return jsonify({
                'error': 'Job data must be an array',
                'code': 'INVALID_FORMAT'
            }), 400
            
        # Process data
        try:
            result = await linkedin_handler.process_scraped_data(job_data)
            
            # Log success
            current_app.logger.info(
                f"Successfully processed {result['metrics']['processed_jobs']} "
                f"out of {result['metrics']['total_jobs']} jobs"
            )
            
            return jsonify({
                'success': True,
                'metrics': result['metrics'],
                'timestamp': result['data']['last_updated']
            })
            
        except JobDataError as e:
            current_app.logger.error(f"Job data processing error: {str(e)}")
            return jsonify({
                'error': str(e),
                'code': 'PROCESSING_ERROR'
            }), 422
            
    except Exception as e:
        current_app.logger.error(f"Unexpected error in LinkedIn update: {str(e)}")
        return jsonify({
            'error': "Internal server error",
            'code': 'INTERNAL_ERROR'
        }), 500

@sage_bp.route('/chat', methods=['POST'])
async def chat():
    """Main chat endpoint"""
    try:
        data = request.json
        message = data.get('message')
        chat_type = data.get('type', 'general')
        
        if not message:
            return jsonify({
                'error': 'No message provided'
            }), 400
            
        response = await sage_ai.get_career_advice(chat_type, message)
        
        return jsonify({
            'response': response,
            'type': chat_type
        })
    except ValueError as e:
        return jsonify({
            'error': str(e),
            'code': Config.ERROR_CODES['INVALID_INPUT'],
            'message': Config.ERROR_MESSAGES[Config.ERROR_CODES['INVALID_INPUT']]
        }), 400
    except Exception as e:
        return jsonify({
            'error': str(e),
            'code': Config.ERROR_CODES['API_ERROR'],
            'message': Config.ERROR_MESSAGES[Config.ERROR_CODES['API_ERROR']]
        }), 500



@sage_bp.route('/recommend-courses', methods=['POST'])
async def recommend_courses():
    """Get personalized course recommendations with time analysis"""
    try:
        data = request.json
        user_skills = data.get('skills', [])
        career_goal = data.get('career_goal')
        available_hours = data.get('available_hours', 10)
        try:
            pace = LearningPace(data.get('learning_pace', 'moderate'))
        except ValueError:
            return jsonify({
                'error': 'Invalid learning pace. Must be one of: slow, moderate, fast'
            }), 400
        commitments = data.get('commitments', [])
        learning_style = data.get('learning_style')
        
        if not career_goal:
            return jsonify({
                'error': 'Career goal is required'
            }), 400
            
        recommendations = await course_recommender.get_personalized_courses(
            user_skills=user_skills,
            career_goal=career_goal,
            available_hours_per_week=available_hours,
            learning_pace=pace,
            current_commitments=commitments,
            preferred_learning_style=learning_style
        )
        
        return jsonify(recommendations)
        
    except Exception as e:
        return jsonify({
            'error': f"An error occurred: {str(e)}"
        }), 500




@sage_bp.route('/analyze-schedule', methods=['POST'])
async def analyze_schedule():
    """Analyze user's schedule for learning"""
    try:
        data = request.json
        hours = data.get('available_hours', 10)
        pace = LearningPace(data.get('learning_pace', 'moderate'))
        commitments = data.get('commitments', [])
        
        analysis = await course_recommender.analyze_user_schedule(
            available_hours_per_week=hours,
            preferred_pace=pace,
            current_commitments=commitments
        )
        
        return jsonify(analysis)
        
    except Exception as e:
        return jsonify({
            'error': f"An error occurred: {str(e)}"
        }), 500

@sage_bp.route('/get-time-breakdown', methods=['POST'])
async def get_time_breakdown():
    """Get detailed time breakdown for learning"""
    try:
        data = request.json
        hours = data.get('available_hours', 10)
        pace = LearningPace(data.get('learning_pace', 'moderate'))
        
        breakdown = course_recommender._generate_time_breakdown(
            available_hours=hours,
            pace=pace
        )
        
        return jsonify({
            'success': True,
            'breakdown': breakdown
        })
        
    except Exception as e:
        return jsonify({
            'error': f"An error occurred: {str(e)}"
        }), 500

@sage_bp.route('/match-jobs', methods=['POST'])
async def match_jobs():
    """Match jobs to user's skills"""
    try:
        data = request.json
        user_skills = data.get('skills', [])
        job_listings = data.get('job_listings', [])
        experience_level = data.get('experience_level', 'entry')
        
        match_level = {
            'entry': JobMatchLevel.ENTRY,
            'intermediate': JobMatchLevel.INTERMEDIATE,
            'senior': JobMatchLevel.SENIOR
        }.get(experience_level, JobMatchLevel.ENTRY)
        
        matched_jobs = await course_recommender.match_jobs_to_skills(
            user_skills=user_skills,
            job_listings=job_listings,
            experience_level=match_level
        )
        
        return jsonify(matched_jobs)
        
    except Exception as e:
        return jsonify({
            'error': f"An error occurred: {str(e)}"
        }), 500

@sage_bp.route('/career-roadmap', methods=['POST'])
async def career_roadmap():
    """Create a career roadmap from current skills to target job"""
    try:
        data = request.json
        current_skills = data.get('current_skills', [])
        target_job = data.get('target_job', {})
        available_hours = data.get('available_hours', 10)
        
        roadmap = await course_recommender.get_career_roadmap(
            current_skills=current_skills,
            target_job=target_job,
            available_hours=available_hours
        )
        
        return jsonify(roadmap)
        
    except Exception as e:
        return jsonify({
            'error': f"An error occurred: {str(e)}"
        }), 500