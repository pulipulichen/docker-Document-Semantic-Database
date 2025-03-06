from google import genai
import os
from PIL import Image

client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

# 定义英文提示词
prompt=os.getenv('GEMINI_VISION_DESCRIBE_PROMPT')
model=os.getenv('GEMINI_MODEL')

def vision_describe(image):

  response = client.models.generate_content(
      model=model, contents=[prompt, image]
  )
  
  return response.text