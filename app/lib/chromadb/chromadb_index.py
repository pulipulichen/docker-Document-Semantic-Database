from lib.chromadb.get_collection import get_collection

def chromadb_index(
    collection_name,
    ids,
    embeddings,
    documents,
    metadata
):
  if len(embeddings) == 0:
    return False

  collection = get_collection(collection_name)

  collection.upsert(
    documents=documents,
    embeddings=embeddings,
    metadatas=[metadata]*(len(documents)),
    ids=ids
  )

  # print(collection.count())