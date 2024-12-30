from celery import shared_task
from services.jira_service import JiraService
from config import Config
import time
import logging
from services.weaviate_service import WeaviateService
import requests

logger = logging.getLogger(__name__)

@shared_task(name='tasks.test_task')
def test_task():
    time.sleep(5)  # Simulate some work
    return {'status': 'Task completed successfully'}

@shared_task(name='tasks.process_jira_webhook')
def process_jira_webhook(data):
    try:
        # Extract issue ID from webhook data
        issue_id = data['issue']['id']
        
        # Initialize Jira service
        jira_service = JiraService(
            Config.JIRA_URL,
            Config.JIRA_USERNAME,
            Config.JIRA_API_TOKEN
        )
        
        # Fetch complete issue details
        issue_details = jira_service.get_issue_details(issue_id)
        
        # Initialize Weaviate service and store data
        weaviate_service = WeaviateService()
        try:
            # Insert issue with embedded comments
            issue_uuid = weaviate_service.insert_issue(issue_details)
            
            logger.info(f"Successfully stored issue {issue_id} in Weaviate")
            return {
                'status': 'success',
                'message': f'Issue {issue_id} processed and stored',
                'issue_uuid': issue_uuid
            }
            
        finally:
            weaviate_service.close()
            
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        return {
            'status': 'error',
            'message': str(e)
        }

@shared_task(name='tasks.process_user_query')
def process_user_query(query):
    try:
        weaviate_service = WeaviateService()
        
        system_prompt = """You are a helpful assistant analyzing Jira issues. 
        Based on the historical data provided, summarize similar issues and their resolutions 
        in a clear, well-structured format. Include:
        1. Relevant ticket references
        Keep the tone professional and focused on providing actionable insights."""


        try:
            collection = weaviate_service.client.collections.get("JiraIssue")

            # URL of the Ollama API endpoint
            url = "http://localhost:11434/api/generate"

            response = collection.query.hybrid(query=query, limit=3)

            tickets = []
            
            for o in response.objects:
                tickets.append(o.properties)

            context = "Context: These are Jira tickets for analyzing webhook functionality."
            prompt = f"{context}\n{tickets}"

            # Prepare the request payload
            data = {
                "model": "tinyllama",
                "prompt": prompt,
                "system": system_prompt,
                "stream": False
            }

            # Headers specifying content type
            headers = {
                "Content-Type": "application/json"
            }

            # Sending POST request to the Ollama API
            response = requests.post(url, json=data, headers=headers)

            if response.status_code == 200:
                value = response.json()
                return {
                    'status': 'success',
                    'summary': value.get("response", "No summary provided"),
                    'timestamp': time.time()
                }
            else:
                return {
                    'status': 'error',
                    'message': response.text,
                    'status_code': response.status_code,
                    'timestamp': time.time()
                }

        except Exception as e:
            # Handle exceptions during processing
            return {
                'status': 'error',
                'message': f"An error occurred during processing: {str(e)}",
                'timestamp': time.time()
            }

        finally:
            weaviate_service.close()

    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        return {
            'status': 'error',
            'message': str(e)
        }