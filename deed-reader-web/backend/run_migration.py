#!/usr/bin/env python3
"""
Deed Reader Pro - Migration Runner
----------------------------------
Runs both Flask (legacy) and FastAPI (new) servers during migration period.

Flask runs on port 5000 (default)
FastAPI runs on port 8000 (new)

A reverse proxy or the frontend can gradually switch endpoints from Flask to FastAPI.
"""

import os
import sys
import logging
import subprocess
import threading
import time
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def run_flask_server():
    """Run the Flask server in a subprocess."""
    logger.info("Starting Flask server on port 5000...")
    try:
        # Run Flask app
        env = os.environ.copy()
        env['FLASK_APP'] = 'app.py'
        env['FLASK_ENV'] = 'development'
        
        process = subprocess.Popen(
            [sys.executable, 'app.py'],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        # Stream output
        for line in iter(process.stdout.readline, ''):
            if line:
                print(f"[FLASK] {line.strip()}")
        
        process.wait()
        
    except Exception as e:
        logger.error(f"Flask server error: {e}")


def run_fastapi_server():
    """Run the FastAPI server in a subprocess."""
    logger.info("Starting FastAPI server on port 8000...")
    try:
        # Run FastAPI app with uvicorn
        process = subprocess.Popen(
            [
                sys.executable, '-m', 'uvicorn',
                'main:app',
                '--host', '0.0.0.0',
                '--port', '8000',
                '--reload',
                '--log-level', 'info'
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        # Stream output
        for line in iter(process.stdout.readline, ''):
            if line:
                print(f"[FASTAPI] {line.strip()}")
        
        process.wait()
        
    except Exception as e:
        logger.error(f"FastAPI server error: {e}")


def main():
    """Run both servers concurrently."""
    logger.info("=" * 60)
    logger.info("Deed Reader Pro - Migration Mode")
    logger.info("=" * 60)
    logger.info("Flask (legacy) will run on: http://localhost:5000")
    logger.info("FastAPI (new) will run on: http://localhost:8000")
    logger.info("FastAPI docs available at: http://localhost:8000/api/docs")
    logger.info("=" * 60)
    
    # Check if required files exist
    if not Path('app.py').exists():
        logger.error("Flask app.py not found!")
        return 1
    
    if not Path('main.py').exists():
        logger.error("FastAPI main.py not found!")
        return 1
    
    # Create threads for each server
    flask_thread = threading.Thread(target=run_flask_server, name="FlaskServer")
    fastapi_thread = threading.Thread(target=run_fastapi_server, name="FastAPIServer")
    
    # Start both servers
    flask_thread.start()
    time.sleep(2)  # Give Flask a moment to start
    fastapi_thread.start()
    
    try:
        # Wait for both threads
        flask_thread.join()
        fastapi_thread.join()
    except KeyboardInterrupt:
        logger.info("\nShutting down both servers...")
        # The subprocesses will be terminated when the main process exits
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 