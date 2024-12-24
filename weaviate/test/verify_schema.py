import weaviate

# Connect to Weaviate instance using the updated syntax
client = weaviate.Client(
    url="http://localhost:8080",  # Replace with your Weaviate instance URL
)

# Get and print the schema
schema = client.schema.get()
print("Current Schema:")
print(schema)