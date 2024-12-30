import weaviate
import os
from pathlib import Path
from dotenv import load_dotenv


env_path = Path('../../backend/.env')
load_dotenv(dotenv_path=env_path)

print(os.getenv('COHERE_API_KEY'))

client = weaviate.connect_to_local(
    host="localhost",
    port=8080,
    grpc_port=50051,
    headers={
        "X-Cohere-Api-Key": os.environ["COHERE_API_KEY"]
    }
)

response = client.collections.list_all(simple=False)
# response = client.collections.get("JiraIssue")

print(response)

client.close()