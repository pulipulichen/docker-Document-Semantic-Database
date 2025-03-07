from fastapi import FastAPI, UploadFile, File, Form
from typing import Optional

from lib.embedding.text_to_embedding import text_to_embedding

from lib.embedding.parse_json import parse_json
from lib.file.file_to_documents import file_to_documents


from lib.chromadb.chromadb_query import chromadb_query
from lib.chromadb.chromadb_query import chromadb_query

from lib.process_index import process_index

from lib.file.save_upload_file import save_upload_file

import asyncio

app = FastAPI()
@app.post("/index")
async def index(
        knowledge_id: str = Form('knowledge_base'),
        item_id: Optional[str] = Form(None),
        metadata: Optional[str] = Form(None),
        file: Optional[UploadFile] = File(None),
        document: Optional[str] = Form(None),
        index_config: Optional[str] = Form(None),       
    ):

    file_ext, file_path, filename = save_upload_file(file)
    
    asyncio.create_task(process_index(
        knowledge_id,
        item_id,
        metadata,
        file_path,
        filename,
        document,
        index_config
    ))  # 讓 process_index() 在背景執行

    return True


@app.post("/query")
async def query(
        knowledge_id: str = Form('knowledge_base'),
        metadata: Optional[str] = Form(None),
        file: Optional[UploadFile] = File(None),
        document: Optional[str] = Form(None),
        query: Optional[str] = Form(None),
        index_config: Optional[str] = Form(None),
        query_config: Optional[str] = Form(None),
        retrieval_setting: Optional[str] = Form(None)
    ):

    file_ext, file_path, filename = save_upload_file(file)

    metadata = parse_json(metadata)

    index_config = parse_json(index_config)
    query_config = parse_json(query_config)
    retrieval_setting = parse_json(retrieval_setting)

    query_config.update(retrieval_setting)

    if query is not None:
        if document is None:
            document = query
        else:
            document = document + query

    # print(query_config)
    documents = await file_to_documents(document, file_path, index_config)

    # =================================================================

    embeddings = []
    if documents and len(documents) > 0:
        # convert each document to embedding
        for doc in documents:
            embeddings.append(text_to_embedding(doc))

    # =================================================================

    results = chromadb_query(
        knowledge_id,
        embeddings,
        metadata,
        query_config
    )

    # =================================================================

    return results
