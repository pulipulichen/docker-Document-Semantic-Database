from fastapi import FastAPI, File, UploadFile, HTTPException, Form

import os
import uvicorn
from starlette.responses import JSONResponse

from lib.elements_to_markdown import elements_to_markdown

from lib.save_upload_file import save_upload_file

from typing import Optional
from lib.parse_json import parse_json
from lib.file_path_to_elements import file_path_to_elements

from lib.app_cors import app_cors

# 初始化 FastAPI
app = FastAPI()
app_cors(app)

@app.post("/process")
async def process_file(
    file: UploadFile = File(...),
    chunk_config: Optional[str] = Form(None),
    ):

    chunk_config = parse_json(chunk_config)

    # =================================================================

    # https://docs.unstructured.io/open-source/core-functionality/partitioning#partition
    file_ext, file_path = save_upload_file(file)

    elements = file_path_to_elements(file_ext, file_path, chunk_config)
    markdown_result = elements_to_markdown(file_ext, elements, chunk_config)

    # 刪除上傳的檔案
    os.remove(file_path)

    # 返回 JSON 資料
    return JSONResponse(content={"status": "success", "data": markdown_result})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
