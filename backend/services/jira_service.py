# from celery import shared_task
# import weaviate
# from config import Config
# import logging

# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # Initialize Weaviate client
# client = weaviate.Client(
#     url=Config.WEAVIATE_URL,
#     auth_client_secret=weaviate.AuthApiKey(api_key=Config.WEAVIATE_API_KEY) if Config.WEAVIATE_API_KEY else None
# )

# # Define the class schema if it doesn't exist
# class_obj = {
#     "class": "Ticket",
#     "vectorizer": "text2vec-transformers",  # Uses the default transformer model
#     "moduleConfig": {
#         "text2vec-transformers": {
#             "vectorizeClassName": False
#         }
#     },
#     "properties": [
#         {
#             "name": "title",
#             "dataType": ["text"],
#             "moduleConfig": {
#                 "text2vec-transformers": {
#                     "skip": False,
#                     "vectorizePropertyName": False
#                 }
#             }
#         },
#         {
#             "name": "description",
#             "dataType": ["text"],
#             "moduleConfig": {
#                 "text2vec-transformers": {
#                     "skip": False,
#                     "vectorizePropertyName": False
#                 }
#             }
#         },
#         {
#             "name": "resolution",
#             "dataType": ["text"],
#             "moduleConfig": {
#                 "text2vec-transformers": {
#                     "skip": False,
#                     "vectorizePropertyName": False
#                 }
#             }
#         },
#         {
#             "name": "key",
#             "dataType": ["string"],
#             "moduleConfig": {
#                 "text2vec-transformers": {
#                     "skip": True
#                 }
#             }
#         }
#     ]
# }

# # Create schema if it doesn't exist
# try:
#     if not client.schema.exists("Ticket"):
#         client.schema.create_class(class_obj)
#         logger.info("Created Ticket schema in Weaviate")
# except Exception as e:
#     logger.error(f"Error creating schema: {str(e)}")

# @shared_task
# def process_jira_webhook(data):
#     """Process incoming Jira webhook data"""
#     try:
#         if data.get('issue_event_type_name') == 'issue_closed':
#             issue = data['issue']
            
#             # Extract relevant information
#             ticket_data = {
#                 'title': issue['fields']['summary'],
#                 'description': issue['fields']['description'] or "",
#                 'resolution': issue['fields'].get('resolution', {}).get('description', "No resolution provided"),
#                 'key': issue['key']
#             }
            
#             # Store in Weaviate - it will automatically generate embeddings
#             try:
#                 client.data_object.create(
#                     class_name="Ticket",
#                     data_object=ticket_data
#                 )
#                 logger.info(f"Successfully processed ticket {ticket_data['key']}")
#                 return {'status': 'processed', 'key': ticket_data['key']}
#             except Exception as e:
#                 logger.error(f"Error storing ticket in Weaviate: {str(e)}")
#                 return {'status': 'error', 'message': str(e)}
        
#         return {'status': 'ignored', 'reason': 'not a closed ticket event'}
    
#     except Exception as e:
#         logger.error(f"Error processing webhook: {str(e)}")
#         return {'status': 'error', 'message': str(e)}
