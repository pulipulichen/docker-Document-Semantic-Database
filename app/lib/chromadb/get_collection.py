import chromadb

client = None

def get_collection(collection_name):
  global client
  if client is None:
    client = chromadb.HttpClient(host='chromadb', port=8000)

  return client.get_or_create_collection(
      name=collection_name, 
      metadata={"hnsw:space": "cosine"}
  )