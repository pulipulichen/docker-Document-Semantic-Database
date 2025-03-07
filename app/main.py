from fastapi import FastAPI, UploadFile, File, Form, Request
from typing import Optional

from lib.chromadb.chromadb_ready import chromadb_ready

from lib.process_index import process_index
from lib.process_query import process_query

from lib.file.save_upload_file import save_upload_file

import asyncio

app = FastAPI()
@app.post("/index")
async def index(
        knowledge_id: str = Form('knowledge_base'),
        item_id: Optional[str] = Form(None),
        title: Optional[str] = Form(None),
        metadata: Optional[str] = Form(None),
        file: Optional[UploadFile] = File(None),
        content: Optional[str] = Form(None),
        document: Optional[str] = Form(None),
        index_config: Optional[str] = Form(None),       
    ):

    # =================================================================
    # Adapted for External Knowledge API https://docs.dify.ai/guides/knowledge-base/external-knowledge-api-documentation

    if title is not None and item_id is None:
        item_id = title

    if content is not None:
        if document is None:
            document = content
        else:
            document = document + content

    # =================================================================

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
@app.post("/retrieval")
async def query(
        request: Request,
        knowledge_id: str = Form(None),
        metadata: Optional[str] = Form(None),
        file: Optional[UploadFile] = File(None),
        document: Optional[str] = Form(None),
        item_id: Optional[str] = Form(None),
        title: Optional[str] = Form(None),
        query: Optional[str] = Form(None),
        index_config: Optional[str] = Form(None),
        query_config: Optional[str] = Form(None),
        retrieval_setting: Optional[str] = Form(None)
    ):

    return await process_query(
        request,
        knowledge_id,
        metadata,
        file,
        document,
        item_id,
        title,
        query,
        index_config,
        query_config,
        retrieval_setting
    )

@app.get("/knowledge_base/{knowledge_id}/{item_id}/")
async def check_ready(
        knowledge_id: str, 
        item_id: str
    ):
    return chromadb_ready(knowledge_id, item_id)
