from celery import shared_task
import weaviate
from config import Config
import logging
from requests.auth import HTTPBasicAuth
import requests
from flask import current_app

class JiraService:
    def __init__(self, base_url, username, api_token):
        self.base_url = base_url
        self.auth = HTTPBasicAuth(username, api_token)
        self.headers = {"Accept": "application/json"}

    def get_issue_details(self, issue_id):
        """Fetch complete issue details from Jira API"""
        url = f"{self.base_url}/rest/api/3/issue/{issue_id}"
        response = requests.get(url, headers=self.headers, auth=self.auth)
        response.raise_for_status()
        return response.json()