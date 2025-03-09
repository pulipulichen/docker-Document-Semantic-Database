
from .convert_metadata_to_where import convert_metadata_to_where
from .filter_by_min_distance import filter_by_min_distance
from .get_collection import get_collection
import os

from .external_knowledge_response import external_knowledge_response



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

  if 'top_k' in query_config:
    max_results = int(query_config['top_k'])

  result_width = int(os.getenv('CHROMADB_QUERY_RESULT_WIDTH', 30))
  if 'result_width' in query_config:
    result_width = int(query_config['result_width'])

  item_distinct = os.getenv('CHROMADB_QUERY_ITEM_DISTINCT', True)
  if item_distinct == False or item_distinct == 'false' or item_distinct == 'False':
    item_distinct = False
  if 'item_distinct' in query_config:
    item_distinct = bool(query_config['item_distinct'])
  
  # print(item_distinct, os.getenv('CHROMADB_QUERY_ITEM_DISTINCT', True), bool('false'))
  # item_distinct = True
  

  score_threshold = float(os.getenv('CHROMADB_QUERY_SCORE_THRESHOLD', 0.0))
  if 'score_threshold' in query_config:
    score_threshold = float(query_config['score_threshold'])

  # =================================================================
  
  n_results = result_width
  if item_distinct is False:
    n_results = max_results

  # =================================================================
 
  collection = get_collection(collection_name)

  # print(collection_name, n_results, metadata, len(embeddings[0]), embeddings[0][:5])

  chromadb_results = collection.query(
    query_embeddings=embeddings,
    where=convert_metadata_to_where(metadata),
    n_results=n_results
  )

  # print(chromadb_results)
  # print(item_distinct)


  if item_distinct is False:
    formated_results = {
      "documents": chromadb_results["documents"][0],
      "metadatas": chromadb_results["metadatas"][0],
      "distances": chromadb_results["distances"][0],
    }
  else:
    formated_results = filter_by_min_distance(chromadb_results, max_results)

  # print(collection.count())
  return external_knowledge_response(formated_results, score_threshold)