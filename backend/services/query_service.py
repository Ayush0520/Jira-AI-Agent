# from celery import shared_task
# import weaviate
# from transformers import AutoModelForCausalLM, AutoTokenizer
# from config import Config
# from .vector_service import create_embeddings

# client = weaviate.Client(Config.WEAVIATE_URL)
# model = AutoModelForCausalLM.from_pretrained(Config.MODEL_PATH)
# tokenizer = AutoTokenizer.from_pretrained(Config.MODEL_PATH)

# @shared_task
# def process_user_query(query):
#     # Create query embeddings
#     query_vector = create_embeddings(query)
    
#     # Hybrid search in Weaviate
#     response = client.query.get(
#         "Ticket",
#         ["title", "description", "resolution", "key"]
#     ).with_hybrid(
#         query=query,
#         vector=query_vector,
#         alpha=0.5
#     ).with_limit(5).do()
    
#     # Extract context from similar tickets
#     context = ""
#     for ticket in response['data']['Get']['Ticket']:
#         context += f"Ticket {ticket['key']}:\n"
#         context += f"Title: {ticket['title']}\n"
#         context += f"Resolution: {ticket['resolution']}\n\n"
    
#     # Prepare prompt for LLAMA
#     prompt = f"Based on these similar tickets:\n{context}\nQuestion: {query}\nAnswer:"
    
#     # Generate response using LLAMA
#     inputs = tokenizer(prompt, return_tensors="pt")
#     outputs = model.generate(**inputs, max_length=500)
#     response = tokenizer.decode(outputs[0])
    
#     return {'response': response}
