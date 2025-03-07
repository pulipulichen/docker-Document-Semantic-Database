import chromadb

client = None


def chromadb_index(
    collection_name,
    ids,
    embeddings,
    documents,
    metadata
):
  if len(embeddings) == 0:
    return False

  global client
  if client is None:
    client = chromadb.HttpClient(host='chromadb', port=8000)

  collection = client.get_or_create_collection(name=collection_name)

  collection.upsert(
    documents=documents,
    embeddings=embeddings,
    metadatas=[metadata]*(len(documents)),
    ids=ids
  )

  # print(collection.count())