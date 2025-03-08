from .file.file_to_documents import file_to_documents
from .file.file_to_item_id import file_to_item_id

from .chromadb.chromadb_index import chromadb_index
from .chromadb.chromadb_item_delete import chromadb_item_delete
from .embedding.parse_json import parse_json

from .embedding.text_to_embedding import text_to_embedding

async def process_index(
        knowledge_id,
        item_id,
        metadata,
        file_path,
        filename,
        document,
        index_config
):


    index_config = parse_json(index_config)

    # ======================

    documents = await file_to_documents(document, file_path, index_config)
    item_id = file_to_item_id(item_id, filename)

    # =================================================================

    embeddings = []
    ids = []
    if documents and len(documents) > 0:
        # convert each document to embedding
        for index, doc in enumerate(documents):
            embeddings.append(text_to_embedding(doc))
            if not item_id:
                item_id = doc.strip()[:20]
            ids.append(item_id + '_' + str(index))

    # =================================================================

    metadata = parse_json(metadata, item_id)

    chromadb_item_delete(
        knowledge_id,
        item_id
    )

    chromadb_index(
        knowledge_id,
        ids,
        embeddings,
        documents,
        metadata
    )
    

    # =================================================================

    # return {
    #     # "filename": file.filename, 
    #     # "embedding": embedding, 
    #     "document": document,
    #     "parsed_metadata": metadata,
    #     "collection_name": collection_name,
    #     "item_id": item_id
    # }

    print({
        "status": "success",
        "knowledge_id": knowledge_id,
        "item_id": item_id,
        "ids": ids,
        "metadata": metadata
    })