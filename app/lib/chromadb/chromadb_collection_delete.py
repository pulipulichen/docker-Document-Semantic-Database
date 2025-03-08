import chromadb
import os

def chromadb_collection_delete(
    collection_name
):
  
  chromadb_host = os.getenv('CHROMADB_HOST', 'chromadb')
  chromadb_port = int(os.getenv('CHROMADB_PORT', 8000))
  
  client = chromadb.HttpClient(host=chromadb_host, port=chromadb_port)
  client.delete_collection(name=collection_name)

  return True