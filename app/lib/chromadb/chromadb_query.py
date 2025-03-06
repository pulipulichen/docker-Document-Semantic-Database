import chromadb
from lib.chromadb.convert_metadata_to_where import convert_metadata_to_where
from lib.chromadb.filter_by_min_distance import filter_by_min_distance

client = None

def chromadb_query(
    collection_name,
    embeddings,
    metadata,
    max_results
):
  global client
  if client is None:
    client = chromadb.HttpClient(host='chromadb', port=8000)

  collection = client.get_or_create_collection(name=collection_name)

  results = collection.query(
    query_embeddings=embeddings,
    where=convert_metadata_to_where(metadata),
    n_results=max_results
  )

  return filter_by_min_distance(results)

  # print(collection.count())