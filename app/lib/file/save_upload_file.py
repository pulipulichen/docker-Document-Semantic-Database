import os
import uuid
import shutil
import requests

# 設定上傳資料夾
UPLOAD_FOLDER = "/tmp/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # 確保資料夾存在

def save_upload_file(file, download_url):
    # 如果沒有上傳檔案，則從 `download_url` 下載
    if not file:
        if not download_url:
            return None, None, None  # 若 `file` 和 `download_url` 都無效，返回 None
        
        # 取得遠端檔案的副檔名
        file_ext = os.path.splitext(download_url)[1].split("?")[0].split("#")[0].lower()
        if not file_ext:
            file_ext = ".bin"  # 若無副檔名，則預設為 `.bin`

        random_filename = f"{uuid.uuid4().hex}{file_ext}"  # 產生隨機檔名
        file_path = os.path.join(UPLOAD_FOLDER, random_filename)

        # 確保目標資料夾存在
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        try:
            # 下載檔案
            response = requests.get(download_url, stream=True, timeout=10)
            response.raise_for_status()  # 檢查請求是否成功

            # 存檔
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(response.raw, buffer)

            print(f"已下載檔案至: {file_path}")
            return file_ext, file_path, os.path.basename(download_url)

        except requests.exceptions.RequestException as e:
            print(f"下載檔案失敗: {e}")
            return None, None, None

    file_ext = os.path.splitext(file.filename)[1].lower()  # 取得副檔名
    random_filename = f"{uuid.uuid4().hex}{file_ext}"  # 產生隨機檔名
    file_path = os.path.join(UPLOAD_FOLDER, random_filename)

    # 確保目標資料夾存在
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    # 存檔
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        # buffer.write(file.file.read())  # 直接讀取檔案內容步的檔案內容

    # print(file_path)
    # print(file.filename)
    # print(file.content_type)
    # print(file.size)
    # print(os.path.getsize(file_path))
    # print(os.path.getsize('/app/test/example.pdf'))
    

    return file_ext, file_path, file.filename