import os
import requests
from tqdm import tqdm

CHECKPOINT_PATH = os.path.join("/data/models/", os.getenv("SAM_CHECKPOINT_NAME", "SAM_CHECKPOINT_NAME"))
CHECKPOINT_URL = os.getenv("SAM_CHECKPOINT_URL", "SAM_CHECKPOINT_URL")
# 確保權重檔案存在，否則下載
def download_checkpoint():
  url = CHECKPOINT_URL
  save_path = CHECKPOINT_PATH
  if not os.path.exists(save_path):
      print(f"Checkpoing file {save_path} is not existed. Start to download...")
      response = requests.get(url, stream=True)
      total_size = int(response.headers.get("content-length", 0))
      with open(save_path, "wb") as file, tqdm(
          desc=f"Downloading {os.path.basename(save_path)}",
          total=total_size,
          unit="B",
          unit_scale=True,
          unit_divisor=1024,
      ) as bar:
          for data in response.iter_content(chunk_size=1024):
              file.write(data)
              bar.update(len(data))
      print(f"Download finished: {save_path}")
  else:
      print(f"Checkpoing file {save_path} is existed.")
