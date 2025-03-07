from lib.embedding.is_image import is_image
from lib.embedding.vision_describe import vision_describe

import requests

UNSTRUCTURED_API_URL = "http://unstructured:8080/process"

def file_to_documents(document, file):
   documents = []
   if document:
      documents.append(document)

   if file is None:
      return documents

   # ======================

   image_file = is_image(file)
  
   if image_file is not False:
      documents.append(vision_describe(image_file))
      return documents

   # ======================

   files = {'file': (file.filename, file.file.read(), file.content_type)}
   response = requests.post(UNSTRUCTURED_API_URL, files=files)

   # print(response.json())

   # 印出回應
   if response.status_code == 200:
      response_json = response.json()
      if response_json['data']:
         documents = documents + response_json['data']
   else:
      print(response)
      raise ValueError('Invalid response')

   # ======================

   return documents