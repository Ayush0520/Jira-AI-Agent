#!/bin/bash

# Start Redis if not running
sudo service redis-server start

# Start Celery worker in background (Updated command)
celery -A celery_app worker --loglevel=info &

# Start Flask application with gunicorn
gunicorn -c gunicorn_config.py app:app