import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Redis Configuration
    REDIS_HOST = 'localhost'
    REDIS_PORT = 6379
    
    # Celery Configuration
    CELERY_BROKER_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'
    CELERY_RESULT_BACKEND = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'
    
    # Weaviate Configuration
    WEAVIATE_URL = os.getenv('WEAVIATE_URL', 'http://localhost:8080')
    
    # JIRA Configuration
    JIRA_URL = os.getenv('JIRA_URL')
    JIRA_USERNAME = os.getenv('JIRA_USERNAME')
    JIRA_API_TOKEN = os.getenv('JIRA_API_TOKEN')
