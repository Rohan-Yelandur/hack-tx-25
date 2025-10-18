"""
Main Flask application entry point.
Orchestrates the math explanation backend with Gemini, Eleven Labs, and Manim.
"""

import os
import logging
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.exceptions import HTTPException
from config import Config
from routes import api_bp
from utils.helpers import create_response
from services import get_file_storage

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_app(config_class=Config):
    """
    Application factory pattern.
    Creates and configures the Flask application.
    
    Args:
        config_class: Configuration class to use
        
    Returns:
        Configured Flask application
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Validate configuration
    try:
        config_class.validate()
        config_class.ensure_directories()
        logger.info("Configuration validated successfully")
    except ValueError as e:
        logger.error(f"Configuration error: {str(e)}")
        raise
    
    # Enable CORS for all routes
    CORS(app, resources={
        r"/api/*": {
            "origins": "*",
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type"]
        }
    })
    
    # Register blueprints
    app.register_blueprint(api_bp)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Register utility routes
    register_utility_routes(app)
    
    logger.info("Flask application created successfully")
    return app


def register_error_handlers(app):
    """
    Register error handlers for the application.
    
    Args:
        app: Flask application instance
    """
    
    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        """Handle all HTTP exceptions."""
        logger.error(f"HTTP error: {e.code} - {e.description}")
        return jsonify(create_response(
            success=False,
            error=e.description
        )), e.code
    
    @app.errorhandler(404)
    def handle_not_found(e):
        """Handle 404 Not Found errors."""
        return jsonify(create_response(
            success=False,
            error="Endpoint not found"
        )), 404
    
    @app.errorhandler(500)
    def handle_internal_error(e):
        """Handle 500 Internal Server Error."""
        logger.error(f"Internal error: {str(e)}")
        return jsonify(create_response(
            success=False,
            error="Internal server error"
        )), 500
    
    @app.errorhandler(Exception)
    def handle_generic_exception(e):
        """Handle all other exceptions."""
        logger.error(f"Unhandled exception: {str(e)}", exc_info=True)
        return jsonify(create_response(
            success=False,
            error="An unexpected error occurred"
        )), 500


def register_utility_routes(app):
    """
    Register utility routes for the application.
    
    Args:
        app: Flask application instance
    """
    
    @app.route('/')
    def index():
        """Root endpoint with API information."""
        return jsonify({
            'name': 'Math Explanation Backend',
            'version': '1.0.0',
            'description': 'AI-powered math explanation generator with video and audio',
            'endpoints': {
                'solve_text': '/api/solve_text',
                'solve_pdf': '/api/solve_pdf',
                'health': '/health',
                'status': '/status'
            }
        })
    
    @app.route('/health')
    def health():
        """Health check endpoint."""
        return jsonify(create_response(
            success=True,
            message="Service is healthy",
            data={'status': 'ok'}
        ))
    
    @app.route('/status')
    def status():
        """Detailed status endpoint with service information."""
        try:
            file_storage = get_file_storage()
            storage_stats = file_storage.get_storage_stats()
            
            return jsonify(create_response(
                success=True,
                message="Service status",
                data={
                    'status': 'running',
                    'services': {
                        'gemini': 'configured' if Config.GEMINI_API_KEY else 'not configured',
                        'eleven_labs': 'configured' if Config.ELEVEN_LABS_API_KEY else 'not configured',
                        'manim': 'available'
                    },
                    'storage': storage_stats
                }
            ))
        except Exception as e:
            logger.error(f"Error getting status: {str(e)}")
            return jsonify(create_response(
                success=False,
                error=str(e)
            )), 500
    
    @app.route('/static/<path:filename>')
    def serve_static(filename):
        """Serve static files (audio, video)."""
        return send_from_directory(Config.STATIC_FOLDER, filename)
    
    @app.route('/api/cleanup', methods=['POST'])
    def cleanup():
        """Manual cleanup endpoint to remove old files."""
        try:
            file_storage = get_file_storage()
            stats = file_storage.cleanup_old_files()
            
            return jsonify(create_response(
                success=True,
                message="Cleanup completed",
                data=stats
            ))
        except Exception as e:
            logger.error(f"Error during cleanup: {str(e)}")
            return jsonify(create_response(
                success=False,
                error=str(e)
            )), 500


# Create the application instance
app = create_app()


if __name__ == '__main__':
    """Run the application."""
    
    # Print startup information
    logger.info("=" * 60)
    logger.info("Math Explanation Backend Starting...")
    logger.info(f"Host: {Config.HOST}")
    logger.info(f"Port: {Config.PORT}")
    logger.info(f"Debug: {Config.DEBUG}")
    logger.info(f"Gemini Model: {Config.GEMINI_MODEL}")
    logger.info(f"Manim Quality: {Config.MANIM_QUALITY}")
    logger.info("=" * 60)
    
    # Perform initial cleanup if configured
    if Config.CLEANUP_OLD_FILES:
        try:
            file_storage = get_file_storage()
            stats = file_storage.cleanup_old_files()
            logger.info(f"Initial cleanup: {sum(stats.values())} files removed")
        except Exception as e:
            logger.warning(f"Initial cleanup failed: {str(e)}")
    
    # Run the application
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )

