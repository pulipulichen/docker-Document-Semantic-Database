import chromadb
from lib.chromadb.convert_metadata_to_where import convert_metadata_to_where
from lib.chromadb.filter_by_min_distance import filter_by_min_distance
import os

client = None

def chromadb_query(
    collection_name,
    embeddings = [],
    metadata = {},
    query_config = {}
):
  if len(embeddings) == 0:
    return False
  
  # =================================================================
  max_results = int(os.getenv('CHROMADB_QUERY_MAX_RESULTS', 5))
  if 'max_results' in query_config:
    max_results = int(query_config['max_results'])

  result_width = int(os.getenv('CHROMADB_QUERY_RESULT_WIDTH', 30))
  if 'result_width' in query_config:
    result_width = int(query_config['result_width'])

  item_distinct = bool(os.getenv('CHROMADB_QUERY_ITEM_DISTINCT', True))
  if 'item_distinct' in query_config:
    item_distinct = bool(query_config['item_distinct'])

  # =================================================================
  
  n_results = result_width
  if item_distinct is False:
    n_results = max_results

  # =================================================================
  global client
  if client is None:
    client = chromadb.HttpClient(host='chromadb', port=8000)

  collection = client.get_or_create_collection(name=collection_name)

  results = collection.query(
    query_embeddings=embeddings,
    where=convert_metadata_to_where(metadata),
    n_results=n_results
  )

  # print(item_distinct)

  if item_distinct is False:
    return {
      "documents": results["documents"][0],
      "metadatas": results["metadatas"][0],
      "distances": results["distances"][0],
    }
  else:
    return filter_by_min_distance(results, max_results)

  # print(collection.count())