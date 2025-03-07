from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import uvicorn
from starlette.responses import JSONResponse

from unstructured.partition.auto import partition
from unstructured.partition.pdf import partition_pdf
from unstructured.partition.ppt import partition_ppt
from unstructured.partition.pptx import partition_pptx
from unstructured.partition.rtf import partition_rtf
from unstructured.partition.doc import partition_doc
from unstructured.partition.docx import partition_docx

from lib.elements_to_markdown import elements_to_markdown

from lib.save_upload_file import save_upload_file

# 初始化 FastAPI
app = FastAPI()

# 允許跨域請求 (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允許所有來源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/process")
async def process_file(file: UploadFile = File(...)):
    file_ext, file_path = save_upload_file(file)

    # https://docs.unstructured.io/open-source/core-functionality/partitioning#partition

    # 根據副檔名決定 partition 方法
    if file_ext in [".pdf"]:
        elements = partition_pdf(
            filename=file_path,
            infer_table_structure=True,
            strategy="auto",
            languages=["chi_tra", "eng", "chi_sim"],
            include_page_breaks=False,
        )
    elif file_ext in [".ppt"]:
        elements = partition_ppt(
            include_page_breaks=False,
        )
    elif file_ext in [".pptx"]:
        elements = partition_pptx(
            include_page_breaks=False,
        )
    elif file_ext in [".rtf"]:
        elements = partition_rtf(
            include_page_breaks=False,
        )
    elif file_ext in [".doc"]:
        elements = partition_doc(
            include_page_breaks=False,
        )
    elif file_ext in [".docx"]:
        elements = partition_docx(
            include_page_breaks=False,
        )
    else:
        elements = partition(filename=file_path)

    markdown_result = elements_to_markdown(elements)

    # 刪除上傳的檔案
    os.remove(file_path)

    # 返回 JSON 資料
    return JSONResponse(content={"status": "success", "data": markdown_result})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
