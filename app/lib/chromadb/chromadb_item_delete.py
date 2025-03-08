
from lib.chromadb.convert_metadata_to_where import convert_metadata_to_where
from lib.chromadb.filter_by_max_distance import filter_by_max_distance
from lib.chromadb.get_collection import get_collection
import os

from .external_knowledge_response import external_knowledge_response

def chromadb_item_delete(
    collection_name,
    item_id
):
  collection = get_collection(collection_name)

  collection.delete(
    where={
      "item_id": item_id
    }
  )

  # print(chromadb_results)
  # print(item_distinct)

  return True