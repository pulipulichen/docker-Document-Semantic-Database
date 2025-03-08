import chromadb
import os

client = None

def get_collection(collection_name):
  global client
  if client is None:
    chromadb_host = os.getenv('CHROMADB_HOST', 'chromadb')
    chromadb_port = int(os.getenv('CHROMADB_PORT', 8000))

    # print("chromadb", chromadb_host, chromadb_port)

    client = chromadb.HttpClient(host=chromadb_host, port=chromadb_port)

  return client.get_or_create_collection(
      name=collection_name, 
      metadata={"hnsw:space": "cosine"}
  )