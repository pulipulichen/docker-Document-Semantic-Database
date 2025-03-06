
import json

def parse_matadata(metadata, item_id = None):
  parsed_metadata = {}

  # ======================
  # Parse metadata JSON if provided
  if metadata:
      try:
          parsed_metadata = json.loads(metadata)
      except json.JSONDecodeError:
          parsed_metadata = {"error": "Invalid JSON format in metadata"}
  
  if item_id:
      parsed_metadata['item_id'] = item_id

  return parsed_metadata