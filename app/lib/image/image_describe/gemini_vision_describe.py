from google import genai
import os
from PIL import Image

import time

client = None

# 定义英文提示词
prompt=os.getenv('VISION_DESCRIBE_PROMPT', 'Describe the content of this image and OCR any text in the image.')
model=os.getenv('GEMINI_MODEL', 'gemini-2.0-flash-lite')

import base64
import mimetypes

def encode_image(file_path):
    # Determine MIME type
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type is None:
        mime_type = "application/octet-stream"  # Fallback if MIME type is unknown

    # Read and encode the file in base64
    with open(file_path, "rb") as image_file:
        encoded_data = base64.b64encode(image_file.read()).decode("utf-8")

    return {"mime_type": mime_type, "data": encoded_data}

def gemini_vision_describe(image_path):

  global client
  if client is None:
    client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
  else:
    time.sleep(3)


  image = Image.open(image_path)

  response = client.models.generate_content(
      model=model, contents=[prompt, image]
  )
  
  return response.text