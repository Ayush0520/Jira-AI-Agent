from flask import Flask, request, jsonify
from celery import Celery
from config import Config
import logging
import tasks  # Import tasks module

app = Flask(__name__)
app.config.from_object(Config)

# Initialize Celery
celery = Celery(
    'tasks',  # Changed to match tasks module name
    broker=app.config['CELERY_BROKER_URL'],
    backend=app.config['CELERY_RESULT_BACKEND']
)

# Load tasks module for registration
celery.config_from_object(app.config)

@app.route('/webhook/jira', methods=['POST'])
def jira_webhook():
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No data received'}), 400

        app.logger.info(f"Received Jira webhook: {data.get('webhookEvent')}")
        
        # Queue the webhook processing task
        task = celery.send_task('tasks.process_jira_webhook', args=[data])
        
        return jsonify({
            'status': 'accepted',
            'task_id': task.id,
            'message': 'Webhook received and processing started'
        }), 202

    except Exception as e:
        app.logger.error(f"Webhook error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/query', methods=['POST'])
def query():
    try:
        data = request.json
        user_query = data.get('query')
        if not user_query:
            return jsonify({'error': 'Query is required'}), 400
        
        # Execute task and wait for result
        task = celery.send_task('tasks.process_user_query', args=[user_query])
        result = task.get(timeout=300)
        
        if result.get('status') == 'error':
            return jsonify(result), 500
            
        return jsonify({
            'status': 'success',
            'summary': result.get('summary'),
            'message': 'Query processed successfully'
        }), 200

    except Exception as e:
        app.logger.error(f"Query error: {str(e)}")
        return jsonify({'error': str(e)}), 500


