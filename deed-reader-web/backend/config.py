"""
Application configuration with timeout and performance settings
"""
import os

class Config:
    # API Timeout Settings
    REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', 300))  # 5 minutes default
    CLAUDE_API_TIMEOUT = int(os.getenv('CLAUDE_API_TIMEOUT', 180))  # 3 minutes for Claude
    
    # Gunicorn/Production Settings
    WORKER_TIMEOUT = int(os.getenv('WORKER_TIMEOUT', 300))  # 5 minutes
    GRACEFUL_TIMEOUT = int(os.getenv('GRACEFUL_TIMEOUT', 30))  # 30 seconds
    
    # File Processing
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 100 * 1024 * 1024))  # 100MB
    CHUNK_SIZE = int(os.getenv('CHUNK_SIZE', 5000))  # Characters per chunk for large docs
    
    # Retry Settings
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', 3))
    RETRY_DELAY = int(os.getenv('RETRY_DELAY', 2))  # seconds
    
    # Performance
    ENABLE_RESPONSE_COMPRESSION = os.getenv('ENABLE_COMPRESSION', 'true').lower() == 'true'
    ENABLE_REQUEST_LOGGING = os.getenv('ENABLE_REQUEST_LOGGING', 'true').lower() == 'true'