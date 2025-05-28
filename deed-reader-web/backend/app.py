#!/usr/bin/env python3
"""
Deed Reader Pro - Web Backend
----------------------------
Flask REST API with OpenAI integration for deed document processing.

Improvements:
- Better configuration management
- Enhanced security headers
- Improved error handling and logging
- More detailed health checks
- Input validation middleware
- Better environment handling
"""

import os
import logging
import json
import time
from datetime import datetime
from flask import Flask, request, jsonify, g
from flask_cors import CORS
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from werkzeug.exceptions import HTTPException
import traceback

# Load environment variables early
load_dotenv()

# Import routes and services
from routes.document_routes import document_bp
from routes.analysis_routes import analysis_bp
from routes.chat_routes import chat_bp
from routes.plotting_routes import plotting_bp
from services.claude_service import ClaudeService


class Config:
    """Application configuration class."""
    
    # Basic Flask config
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(32).hex())
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    # File upload config
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 50 * 1024 * 1024))  # 50MB default
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', os.path.join(os.getcwd(), 'uploads'))
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'tiff', 'bmp'}
    
    # OpenAI config
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
    
    # CORS config
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://127.0.0.1:3000').split(',')
    
    # Logging config
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()
    LOG_FILE = os.getenv('LOG_FILE')
    
    # Security config
    RATE_LIMIT_ENABLED = os.getenv('RATE_LIMIT_ENABLED', 'False').lower() == 'true'
    
    # Health check config
    APP_VERSION = os.getenv('APP_VERSION', '1.0.0')
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')


def setup_logging(config):
    """Configure application logging."""
    handlers = [logging.StreamHandler()]
    
    if config.LOG_FILE:
        handlers.append(logging.FileHandler(config.LOG_FILE))
    
    logging.basicConfig(
        level=getattr(logging, config.LOG_LEVEL),
        format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
        handlers=handlers
    )
    
    # Reduce noise from external libraries
    logging.getLogger('werkzeug').setLevel(logging.WARNING)
    logging.getLogger('httpx').setLevel(logging.WARNING)


def add_security_headers(app):
    """Add security headers to all responses."""
    
    @app.after_request
    def set_security_headers(response):
        # Basic security headers
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # API-specific headers
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        
        return response


def add_request_logging(app):
    """Add request/response logging middleware."""
    
    @app.before_request
    def log_request_info():
        g.start_time = time.time()
        app.logger.info(f"Request: {request.method} {request.url} - IP: {request.remote_addr}")
    
    @app.after_request
    def log_response_info(response):
        duration = time.time() - g.get('start_time', 0)
        app.logger.info(
            f"Response: {response.status_code} - {duration:.3f}s - Size: {response.content_length or 0} bytes"
        )
        return response


def create_app(config_class=Config):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Setup logging
    setup_logging(config_class)
    logger = logging.getLogger(__name__)
    
    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    logger.info(f"Upload directory: {app.config['UPLOAD_FOLDER']}")
    
    # Enable CORS
    CORS(app, origins=app.config['CORS_ORIGINS'])
    logger.info(f"CORS enabled for origins: {app.config['CORS_ORIGINS']}")
    
    # Add security and logging middleware
    add_security_headers(app)
    add_request_logging(app)
    
    # Register blueprints
    app.register_blueprint(document_bp, url_prefix='/api/documents')
    app.register_blueprint(analysis_bp, url_prefix='/api/analysis')
    app.register_blueprint(chat_bp, url_prefix='/api/chat')
    app.register_blueprint(plotting_bp, url_prefix='/api/plotting')
    logger.info("All route blueprints registered")
    
    # Initialize Claude service
    anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
    if ClaudeService.initialize(anthropic_api_key):
        app.config['CLAUDE_ENABLED'] = True
        logger.info("Claude service initialized successfully")
    else:
        app.config['CLAUDE_ENABLED'] = False
        logger.warning("Claude service not available. AI features will be limited.")
    
    # Enhanced health check endpoint
    @app.route('/api/health')
    def health_check():
        """Comprehensive health check endpoint."""
        start_time = time.time()
        health_data = {
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'version': app.config['APP_VERSION'],
            'environment': app.config['ENVIRONMENT'],
            'services': {
                'api': 'healthy',
                'claude': 'healthy' if app.config.get('CLAUDE_ENABLED') else 'disabled',
                'storage': 'healthy' if os.path.exists(app.config['UPLOAD_FOLDER']) else 'error'
            },
            'system': {
                'upload_folder_exists': os.path.exists(app.config['UPLOAD_FOLDER']),
                'upload_folder_writable': os.access(app.config['UPLOAD_FOLDER'], os.W_OK),
                'python_version': os.sys.version.split()[0],
                'max_content_length_mb': app.config['MAX_CONTENT_LENGTH'] // (1024 * 1024)
            }
        }
        
        # Check overall health
        all_services_healthy = all(
            status in ['healthy', 'disabled'] 
            for status in health_data['services'].values()
        )
        
        if not all_services_healthy:
            health_data['status'] = 'degraded'
        
        # Add response time
        health_data['response_time_ms'] = round((time.time() - start_time) * 1000, 2)
        
        status_code = 200 if health_data['status'] == 'healthy' else 503
        return jsonify(health_data), status_code
    
    # API information endpoint
    @app.route('/api/info')
    def api_info():
        """API information and available endpoints."""
        return jsonify({
            'name': 'Deed Reader Pro API',
            'version': app.config['APP_VERSION'],
            'description': 'REST API for deed document processing and analysis',
            'endpoints': {
                'health': '/api/health',
                'documents': '/api/documents',
                'analysis': '/api/analysis', 
                'chat': '/api/chat',
                'plotting': '/api/plotting'
            },
            'features': {
                'file_upload': True,
                'ai_analysis': app.config.get('CLAUDE_ENABLED', False),
                'interactive_chat': app.config.get('CLAUDE_ENABLED', False),
                'coordinate_extraction': app.config.get('CLAUDE_ENABLED', False),
                'plotting': True,
                'ocr_vision': app.config.get('CLAUDE_ENABLED', False)
            },
            'limits': {
                'max_file_size_mb': app.config['MAX_CONTENT_LENGTH'] // (1024 * 1024),
                'allowed_file_types': list(app.config['ALLOWED_EXTENSIONS'])
            }
        })
    
    # Enhanced error handlers
    @app.errorhandler(400)
    def bad_request(error):
        logger.warning(f"Bad request: {error}")
        return jsonify({
            'error': 'Bad Request',
            'message': 'The request was invalid or malformed',
            'status_code': 400,
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }), 400
    
    @app.errorhandler(404)
    def not_found(error):
        logger.warning(f"Not found: {request.url}")
        return jsonify({
            'error': 'Not Found',
            'message': f'The requested resource {request.path} was not found',
            'status_code': 404,
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'available_endpoints': ['/api/health', '/api/info', '/api/documents', '/api/analysis', '/api/chat', '/api/plotting']
        }), 404
    
    @app.errorhandler(413)
    def request_entity_too_large(error):
        max_size_mb = app.config['MAX_CONTENT_LENGTH'] // (1024 * 1024)
        logger.warning(f"File too large: max size is {max_size_mb}MB")
        return jsonify({
            'error': 'Payload Too Large',
            'message': f'File size exceeds the maximum allowed size of {max_size_mb}MB',
            'status_code': 413,
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }), 413
    
    @app.errorhandler(429)
    def rate_limit_exceeded(error):
        logger.warning(f"Rate limit exceeded for IP: {request.remote_addr}")
        return jsonify({
            'error': 'Too Many Requests', 
            'message': 'Rate limit exceeded. Please try again later.',
            'status_code': 429,
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }), 429
    
    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        """Handle all other HTTP exceptions."""
        logger.error(f"HTTP Exception: {e.name} ({e.code}) - {e.description}")
        return jsonify({
            'error': e.name,
            'message': e.description,
            'status_code': e.code,
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }), e.code
    
    @app.errorhandler(500)
    def internal_server_error(error):
        logger.error(f"Internal server error: {error}", exc_info=True)
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred. Please check the logs or contact support.',
            'status_code': 500,
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }), 500
    
    @app.errorhandler(Exception)
    def handle_generic_exception(e):
        """Handle any other unhandled exceptions."""
        error_id = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        logger.error(f"Unhandled exception [{error_id}]: {e}", exc_info=True)
        
        # In production, don't expose internal error details
        if app.config['DEBUG']:
            message = f"Unhandled exception: {str(e)}"
            details = traceback.format_exc()
        else:
            message = f"An unexpected error occurred. Error ID: {error_id}"
            details = None
        
        response_data = {
            'error': 'Unexpected Error',
            'message': message,
            'error_id': error_id,
            'status_code': 500,
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }
        
        if details and app.config['DEBUG']:
            response_data['details'] = details
        
        return jsonify(response_data), 500
    
    return app


# Create the application
app = create_app()

if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logger.info("=" * 50)
    logger.info("Starting Deed Reader Pro Backend")
    logger.info("=" * 50)
    logger.info(f"Version: {app.config['APP_VERSION']}")
    logger.info(f"Environment: {app.config['ENVIRONMENT']}")
    logger.info(f"Debug mode: {app.config['DEBUG']}")
    logger.info(f"Upload folder: {app.config['UPLOAD_FOLDER']}")
    logger.info(f"Claude AI enabled: {app.config.get('CLAUDE_ENABLED', False)}")
    logger.info(f"Max file size: {app.config['MAX_CONTENT_LENGTH'] // (1024 * 1024)}MB")
    logger.info(f"CORS origins: {app.config['CORS_ORIGINS']}")
    logger.info("=" * 50)
    
    # Run the application
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000)),
        debug=app.config['DEBUG'],
        threaded=True
    ) 