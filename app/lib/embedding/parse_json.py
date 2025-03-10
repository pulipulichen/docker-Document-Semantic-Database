
import json

def parse_json(metadata, item_id = None):
  parsed_json = {}

  # ======================
  # Parse metadata JSON if provided
  if metadata:
    if isinstance(metadata, str):
      try:
          parsed_json = json.loads(metadata)
      except json.JSONDecodeError:
          parsed_json = {"error": "Invalid JSON format in metadata"}
    if isinstance(metadata, dict):
       parsed_json = metadata
  
  if item_id:
      parsed_json['item_id'] = item_id

  return parsed_json