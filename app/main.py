from fastapi import FastAPI, UploadFile, File, Form
from typing import Optional

from lib.embedding.text_to_embedding import text_to_embedding

from lib.embedding.parse_matadata import parse_matadata
from lib.file.file_to_documents import file_to_documents

from lib.chromadb.chromadb_index import chromadb_index
from lib.chromadb.chromadb_query import chromadb_query

from lib.file.file_to_item_id import file_to_item_id

app = FastAPI()

@app.post("/index/")
async def index(
        collection_name: str = Form('knowledge_base',),
        item_id: Optional[str] = Form(None),
        metadata: Optional[str] = Form(None),
        file: Optional[UploadFile] = File(None),
        document: Optional[str] = Form(None)        
    ):

    # ======================

    documents = file_to_documents(document, file)
    item_id = file_to_item_id(item_id, file)

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

    metadata = parse_matadata(metadata, item_id)

    chromadb_index(
        collection_name,
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

    return {
        "status": "success",
        "collection": collection_name,
        "item_id": item_id,
        "ids": ids,
        "metadata": metadata
    }


@app.post("/query/")
async def query(
        collection_name: str = Form('knowledge_base',),
        metadata: Optional[str] = Form(None),
        file: Optional[UploadFile] = File(None),
        document: Optional[str] = Form(None),
        max_results: Optional[int] = Form(10)
    ):

    metadata = parse_matadata(metadata)
    documents = file_to_documents(document, file)

    # =================================================================

    embeddings = []
    if documents and len(documents) > 0:
        # convert each document to embedding
        for doc in documents:
            embeddings.append(text_to_embedding(doc))

    # =================================================================

    results = chromadb_query(
        collection_name,
        embeddings,
        metadata,
        max_results
    )

    # =================================================================

    return results
