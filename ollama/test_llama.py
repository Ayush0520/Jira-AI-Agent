import requests

# URL of the Ollama API endpoint
url = "http://localhost:11434/api/generate"

# JSON data to send in the request
data = {
    "model": "tinyllama",
    "prompt": """{'key': 'SCRUM-1', 'assignee': 'Ayush Singh', 'resolutionDate': datetime.datetime(2024, 12, 29, 6, 52, 0, 743000, tzinfo=datetime.timezone(datetime.timedelta(seconds=19800))), 'description': 'This ticket is created to test the webhook setup and observe the data payload sent by Jira when the ticket transitions to the "Closed" state.', 'summary': 'Web Hook Test-1', 'comments': [{'updated': datetime.datetime(2024, 12, 25, 7, 50, 1, 409000, tzinfo=datetime.timezone(datetime.timedelta(seconds=19800))), 'created': datetime.datetime(2024, 12, 25, 7, 50, 1, 409000, tzinfo=datetime.timezone(datetime.timedelta(seconds=19800))), 'author': 'Ayush Singh', 'body': 'Testing Webhook', 'commentID': '10000'}, {'updated': datetime.datetime(2024, 12, 28, 11, 34, 17, 95000, tzinfo=datetime.timezone(datetime.timedelta(seconds=19800))), 'created': datetime.datetime(2024, 12, 28, 11, 34, 17, 95000, tzinfo=datetime.timezone(datetime.timedelta(seconds=19800))), 'author': 'Ayush Singh', 'body': 'Test Comment - 2', 'commentID': '10001'}], 'status': 'Closed', 'issueID': '10000', 'customFields': 'None', 'reporter': 'Ayush Singh', 'attachments': [], 'labels': ['Critical', 'WebhookTesting'], 'updated': datetime.datetime(2024, 12, 29, 6, 52, 0, 753000, tzinfo=datetime.timezone(datetime.timedelta(seconds=19800))), 'created': datetime.datetime(2024, 12, 25, 7, 42, 38, 8000, tzinfo=datetime.timezone(datetime.timedelta(seconds=19800))), 'priority': 'Medium', 'project': 'SCRUM'}""",
    "system": """You are a helpful assistant summarizing Jira tickets. 
        Provide a short summary of the tickets. Include:
        1. A concise description of each ticket
        2. Key details such as assignee, status, and priority
        3. Relevant labels or tags
        Be brief and to the point.""",
    "stream": False
}

# Headers specifying content type
headers = {
    "Content-Type": "application/json"
}

# Sending POST request to the API
response = requests.post(url, json=data, headers=headers)

# Checking if the request was successful (status code 200)
if response.status_code == 200:
    print("Response from Ollama:\n")
    value = response.json()
    print("The value type of response:", type(value))
    # Uncomment the next line if you want to see the entire JSON response
    # print(response.json())
    print(value["response"])
else:
    print(f"Error: {response.status_code} - {response.text}")
