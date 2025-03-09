from fastapi import FastAPI, UploadFile, File, Form, Request, BackgroundTasks, Response
from typing import Optional

from lib.chromadb.chromadb_ready import chromadb_ready
from lib.chromadb.chromadb_collection_delete import chromadb_collection_delete
from lib.chromadb.chromadb_item_delete import chromadb_item_delete

from lib.process_index import process_index
from lib.process_query import process_query

from lib.file.save_upload_file import save_upload_file
import multiprocessing

import asyncio

app = FastAPI()

task_queue = asyncio.Queue()  # 建立排隊隊列
processing = False  # 狀態標記是否有執行中的任務

async def worker():
    """背景工作執行緒，負責依序執行任務"""
    while True:
        task = await task_queue.get()  # 取得下一個排隊任務
        await process_index(*task)  # 執行排隊任務
        task_queue.task_done()  # 標記任務完成

@app.on_event("startup")
async def startup_event():
    """FastAPI 啟動時，開始執行 worker"""
    asyncio.create_task(worker())  # 創建 worker 讓它持續執行

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
        download_url: Optional[str] = Form(None),        
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

    file_ext, file_path, filename = save_upload_file(file, download_url)
    
    # 加入隊列
    await task_queue.put((knowledge_id, item_id, metadata, file_path, filename, document, index_config))

    # print('可以先回覆嗎？')

    return True


@app.post("/query")
@app.post("/retrieval")
async def query(
        request: Request,
        knowledge_id: str = Form(None),
        metadata: Optional[str] = Form(None),
        file: Optional[UploadFile] = File(None),
        download_url: Optional[str] = Form(None),
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
        download_url,
        document,
        item_id,
        title,
        query,
        index_config,
        query_config,
        retrieval_setting
    )

@app.get("/knowledge_base/{knowledge_id}/item/{item_id}/")
async def check_ready(
        knowledge_id: str, 
        item_id: str
    ):
    return chromadb_ready(knowledge_id, item_id)

@app.get("/knowledge_base/{knowledge_id}/delete")
async def delete_collection(
        knowledge_id: str
    ):
    return chromadb_collection_delete(knowledge_id)


@app.get("/knowledge_base/{knowledge_id}/item/{item_Id}/delete")
async def delete_collection(
        knowledge_id: str, 
        item_id: str
    ):
    return chromadb_item_delete(knowledge_id, item_id)