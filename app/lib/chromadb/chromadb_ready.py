
from .convert_metadata_to_where import convert_metadata_to_where
from .filter_by_max_distance import filter_by_max_distance
from .get_collection import get_collection
import os

from .external_knowledge_response import external_knowledge_response



def chromadb_ready(
    collection_name,
    item_id
):
  collection = get_collection(collection_name)

  chromadb_results = collection.get(
    where={
      "item_id": item_id
    }
  )

  # print(chromadb_results)
  # print(item_distinct)

  return (len(chromadb_results["ids"]) > 0)