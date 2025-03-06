from fastapi import UploadFile
from PIL import Image

def is_image(file: UploadFile) -> bool:
    try:
        image_file = Image.open(file.file)
        image_file.verify()  # 嘗試驗證圖片
        file.file.seek(0)  # 重置文件指標，避免影響後續讀取
        return image_file
    except (IOError, SyntaxError):
        return False
