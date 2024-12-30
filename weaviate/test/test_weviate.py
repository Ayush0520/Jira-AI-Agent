import weaviate
import os
from pathlib import Path
from dotenv import load_dotenv
import requests

# URL of the Ollama API endpoint
url = "http://localhost:11434/api/generate"

env_path = Path('../../backend/.env')
load_dotenv(dotenv_path=env_path)
print(os.getenv('COHERE_API_KEY'))

try:
    # Connect to the local Weaviate instance
    client = weaviate.connect_to_local(
        host="localhost",
        port=8080,
        grpc_port=50051,
        headers={
            "X-Cohere-Api-Key": os.environ["COHERE_API_KEY"]
        },
    )
    # Check if Weaviate is ready
    if client.is_ready():
        print("Weaviate is ready!")
    else:
        print("Weaviate is not ready.")

    system_prompt = """You are a helpful assistant analyzing Jira issues. 
        Based on the historical data provided, summarize similar issues and their resolutions 
        in a clear, well-structured format. Include:
        1. Relevant ticket references
        Keep the tone professional and focused on providing actionable insights."""

    
    collection = client.collections.get("JiraIssue")
    response = collection.query.hybrid(query="test the webhook setup", limit=3)

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

    # Check response and print
    if response.status_code == 200:
        print("Response from Ollama:\n")
        value = response.json()
        print(value["response"])
    else:
        print(f"Error: {response.status_code} - {response.text}")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Ensure the client is closed to free up resources
    client.close()
