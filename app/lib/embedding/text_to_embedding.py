import ollama
import os

import time

# Connect to the remote Ollama server
client = None

# Model name
model_name = os.getenv('OLLAMA_EMBEDDING_MODEL', "bge-m3")

def text_to_embedding(text):
  global client
  if client is None:
    client = ollama.Client(host=os.getenv('OLLAMA_HOST', "http://127.0.0.1:11434"))
  else:
    time.sleep(1)

  print('Analysis embedding: ' + text[:50])
  embedding = client.embeddings(model=model_name, prompt=text)
  embedding = embedding["embedding"]

  return embedding