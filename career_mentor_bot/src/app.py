"""
Main Flask application for Sage career mentor bot
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from api.routes import sage_bp
from config import get_config
from models import init_db
import logging
import os
from bot.integrations.linkedin_handler import LinkedInDataHandler
from bot.performance_monitor import PerformanceMonitor
from bot.market_insights import MarketInsights

class SageApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.setup_app()
        
    def setup_app(self):
        # Load configuration
        env = os.getenv('FLASK_ENV', 'development')
        self.app.config.from_object(get_config(env))
        
        # Initialize services
        self.linkedin_handler = LinkedInDataHandler()
        self.performance_monitor = PerformanceMonitor()
        self.market_insights = MarketInsights()
        
        # Configure CORS
        CORS(self.app, resources={
            r"/api/*": {
                "origins": "*",
                "methods": ["GET", "POST", "OPTIONS"],
                "allow_headers": ["Content-Type", "Authorization"]
            }
        })
        
        # Register blueprints
        self.app.register_blueprint(sage_bp, url_prefix='/api/sage')
        
        # Initialize database
        init_db()
        
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
        
        @self.app.route('/api/linkedin/update', methods=['POST'])
        async def update_linkedin_data():
            """Endpoint for web scraper to send LinkedIn data"""
            try:
                data = request.json
                processed_data = await self.linkedin_handler.process_scraped_data(data)
                return jsonify({
                    'success': True,
                    'processed_jobs': len(processed_data['jobs']),
                    'timestamp': processed_data['last_updated']
                })
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500

        # Error handling
        @self.app.errorhandler(404)
        def not_found(error):
            return jsonify({'error': 'Not found'}), 404

        @self.app.errorhandler(500)
        def internal_error(error):
            return jsonify({'error': 'Internal server error'}), 500

def create_app():
    sage_app = SageApp()
    return sage_app.app

if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    app = create_app()
    app.run(debug=True, port=5000)