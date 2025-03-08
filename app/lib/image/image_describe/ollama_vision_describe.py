import ollama
import base64
import os
import time

client = None

# 讀取圖像文件並轉換為 base64 格式
def encode_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def ollama_vision_describe(image_path):
  global client
  if client is None:
    client = ollama.Client(host=os.getenv('OLLAMA_HOST', "http://127.0.0.1:11434"))
  else:
    time.sleep(1)

  with open(image_path, 'rb') as f:
    image_base64 = encode_image(image_path)

  response = ollama.chat(
      model=os.getenv('OLLAMA_VISION_MODEL', 'llava:34b'),
      messages=[
          {
            'role': 'user', 
            'content': os.getenv('VISION_DESCRIBE_PROMPT', 'llava:34b'),
            'images': [image_base64], 
          },
      ]
  )

  # 輸出結果
  return response['message']['content']
