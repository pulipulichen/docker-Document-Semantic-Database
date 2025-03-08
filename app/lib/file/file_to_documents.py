
from .save_upload_file import save_upload_file
from ..image.process_image import process_image

import requests
import os

UNSTRUCTURED_API_ENDPOINT = os.getenv("UNSTRUCTURED_API_ENDPOINT", "http://unstructured:8080/process")

async def file_to_documents(document, file_path, index_config):
   documents = []
   if document:
      documents.append(document)

   if file_path is None:
      return documents


   # ======================

   # file_ext, file_path = save_upload_file(file)

   image_documents = process_image(file_path, index_config)
   if len(image_documents) > 0:
      documents = documents + image_documents

   # ======================

   # ======================

   # file_ext, file_path = save_upload_file(file)

   # print(file.size)
   # print(file_path)
   # # 以 'rb' 模式打開檔案，確保是二進位格式
   # with open(file_path, "rb") as f:
   #     files = {"file": (file_path, f, "application/pdf")}  # 指定 MIME 類型

   #     # 發送 POST 請求
   #     response = requests.post(UNSTRUCTURED_API_URL, files=files)

   # 讀取檔案內容
   # file_content = await file.read()

   # 構造 requests 的 files 參數
   # files = {
   #     "file": (file.filename, open('/app/test/example.pdf'), file.content_type)
   # }

   # # 轉發檔案到 http://127.0.0.1:8000/process
   # response = requests.post(UNSTRUCTURED_API_URL, headers = {"accept": "application/json"}, files=files)

   if len(image_documents) == 0:
      with open(file_path, "rb") as file:
         files = {"file": file}
         data = {"chunk_config": index_config}
         headers = {"accept": "application/json"}
          
         response = requests.post(UNSTRUCTURED_API_ENDPOINT, headers=headers, files=files, data=data)

      # print(response.json())

      # 印出回應
      if response.status_code == 200:
         response_json = response.json()
         if response_json['data']:
            documents = documents + response_json['data']
      else:
         print(response)
         # raise ValueError('Invalid response')

   os.remove(file_path)
   # ======================

   return documents