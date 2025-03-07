from google import genai, generativeai
import os
from PIL import Image

client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

# 定义英文提示词
prompt=os.getenv('GEMINI_VISION_DESCRIBE_PROMPT')
model=os.getenv('GEMINI_MODEL')

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

def vision_describe(image_path):

  image = Image.open(image_path)

  response = client.models.generate_content(
      model=model, contents=[prompt, image]
  )
  
  return response.text