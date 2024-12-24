import weaviate

# Connect to Weaviate instance
client = weaviate.Client("http://localhost:8080")

# Define the schema
schema = {
    "classes": [
        {
            "class": "JiraTicket",
            "description": "Stores JIRA ticket data for semantic search",
            "properties": [
                {
                    "name": "ticket_id",
                    "dataType": ["string"],
                    "description": "Unique identifier for the ticket"
                },
                {
                    "name": "summary",
                    "dataType": ["text"],
                    "description": "Summary of the ticket"
                },
                {
                    "name": "embedding",
                    "dataType": ["blob"],
                    "description": "Vector representation of the ticket"
                },
            ]
        }
    ]
}

# Create the schema in Weaviate
client.schema.create(schema)
print("Schema created successfully!")
