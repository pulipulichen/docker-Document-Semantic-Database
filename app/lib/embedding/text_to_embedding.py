import ollama
import os

import time

# Connect to the remote Ollama server
client = ollama.Client(host=os.getenv('OLLAMA_HOST', "http://127.0.0.1:11434"))

# Model name
model_name = os.getenv('OLLAMA_EMBEDDING_MODEL', "bge-m3")

def text_to_embedding(text):
  time.sleep(3)

  print('Analysis embedding: ' + text)
  embedding = client.embeddings(model=model_name, prompt=text)
  embedding = embedding["embedding"]

  return embedding