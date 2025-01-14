"""
Main Flask application for Sage career mentor bot
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from src.api.routes import sage_bp
from src.config import get_config
from src.models import init_db
import logging
import os
from src.bot.integrations.linkedin_handler import LinkedInDataHandler
from src.bot.performance_monitor import PerformanceMonitor
from src.bot.market_insights import MarketInsights

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
                "origins": ["http://localhost:5173"],
                "methods": ["GET", "POST", "OPTIONS"],
                "allow_headers": ["Content-Type", "Authorization", "X-Requested-With", "Accept", "Origin", "Access-Control-Request-Method", "Access-Control-Request-Headers"]
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

def create_app():
    sage_app = SageApp()
    return sage_app.app

if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    app = create_app()
    app.run(debug=True, port=5000)



