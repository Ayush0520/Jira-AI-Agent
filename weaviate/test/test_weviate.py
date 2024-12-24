import weaviate

try:
    # Connect to the local Weaviate instance
    client = weaviate.connect_to_local(
        host="localhost",
        port=8080,
        grpc_port=50051,
    )
    # Check if Weaviate is ready
    if client.is_ready():
        print("Weaviate is ready!")
    else:
        print("Weaviate is not ready.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Ensure the client is closed to free up resources
    client.close()
