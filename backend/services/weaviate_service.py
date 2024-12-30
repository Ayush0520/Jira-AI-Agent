import weaviate
import logging
from datetime import datetime
from config import Config
import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path('../.env')
load_dotenv(dotenv_path=env_path)
print(os.getenv('COHERE_API_KEY'))

logger = logging.getLogger(__name__)

class WeaviateService:
    def __init__(self):
        self.client = weaviate.connect_to_local(
            host="localhost",
            port=8080,
            grpc_port=50051,
            headers={
                "X-Cohere-Api-Key": os.environ["COHERE_API_KEY"]
            },
            additional_config=weaviate.classes.init.AdditionalConfig(
                timeout=(60, 300),
            )
        )

    def _parse_date(self, date_str):
        if not date_str:
            return None
        try:
            return datetime.fromisoformat(date_str.replace('Z', '+00:00')).isoformat()
        except Exception:
            return None

    def _extract_text_from_doc(self, doc_obj):
        if not doc_obj:
            return None
        text = ""
        if isinstance(doc_obj, dict):
            content = doc_obj.get('content', [])
            for item in content:
                if item.get('type') == 'paragraph':
                    for text_content in item.get('content', []):
                        if text_content.get('type') == 'text':
                            text += text_content.get('text', '') + " "
        return text.strip()

    def insert_issue(self, issue_data):
        try:
            # Process comments
            comments = []
            for comment in issue_data.get('fields', {}).get('comment', {}).get('comments', []):
                comment_obj = {
                    "commentID": str(comment.get('id')),
                    "author": comment.get('author', {}).get('displayName'),
                    "body": self._extract_text_from_doc(comment.get('body')),
                    "created": self._parse_date(comment.get('created')),
                    "updated": self._parse_date(comment.get('updated'))
                }
                comments.append(comment_obj)

            # Prepare issue data
            issue_obj = {
                "issueID": str(issue_data.get('id')),
                "key": issue_data.get('key'),
                "project": issue_data.get('fields', {}).get('project', {}).get('key'),
                "summary": issue_data.get('fields', {}).get('summary'),
                "description": self._extract_text_from_doc(issue_data.get('fields', {}).get('description')),
                "status": issue_data.get('fields', {}).get('status', {}).get('name'),
                "priority": issue_data.get('fields', {}).get('priority', {}).get('name'),
                "labels": issue_data.get('fields', {}).get('labels', []),
                "assignee": issue_data.get('fields', {}).get('assignee', {}).get('displayName'),
                "reporter": issue_data.get('fields', {}).get('reporter', {}).get('displayName'),
                "created": self._parse_date(issue_data.get('fields', {}).get('created')),
                "updated": self._parse_date(issue_data.get('fields', {}).get('updated')),
                "resolutionDate": self._parse_date(issue_data.get('fields', {}).get('resolutiondate')),
                "customFields": str(issue_data.get('fields', {}).get('customfield_10000')),
                "attachments": [att.get('filename') for att in issue_data.get('fields', {}).get('attachment', [])],
                "comments": comments
            }

            # Insert issue
            Issue = self.client.collections.get("JiraIssue")
            issue_uuid = Issue.data.insert(
                properties=issue_obj
            )

            return issue_uuid

        except Exception as e:
            logger.error(f"Error inserting issue: {str(e)}")
            raise

    # Remove insert_comments method as it's no longer needed

    def close(self):
        if self.client:
            self.client = None
