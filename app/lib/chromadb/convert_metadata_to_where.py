
def convert_metadata_to_where(metadata):
  if not metadata:
    return None
  return {key: {"$eq": value} for key, value in metadata.items()}
