import ollama
import os

# Connect to the remote Ollama server
client = ollama.Client(host=os.getenv('OLLAMA_HOST'))

# Model name
model_name = os.getenv('OLLAMA_EMBEDDING_MODEL')

def text_to_embedding(text):
  embedding = client.embeddings(model=model_name, prompt=text)
  return embedding["embedding"]