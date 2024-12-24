from flask import Flask, request, jsonify
from celery import Celery
from config import Config
# from services.jira_service import process_jira_webhook
# from services.query_service import process_user_query

app = Flask(__name__)
app.config.from_object(Config)

# Initialize Celery
celery = Celery(
    app.name,
    broker=app.config['CELERY_BROKER_URL'],
    backend=app.config['CELERY_RESULT_BACKEND']
)

@app.route('/webhook/jira', methods=['POST'])
def jira_webhook():
    data = request.json
    # process_jira_webhook.delay(data)
    return jsonify({'status': 'received'}), 200

@app.route('/api/query', methods=['POST'])
def query():
    # data = request.json
    # user_query = data.get('query')
    # if not user_query:
    #     return jsonify({'error': 'Query is required'}), 400
    
    # result = process_user_query.delay(user_query)
    # return jsonify({'task_id': result.id}), 202
    return jsonify({'status': 'received'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
