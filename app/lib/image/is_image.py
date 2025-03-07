from PIL import Image

def is_image(file_path):
    try:
        image_file = Image.open(file_path)
        image_file.verify()  # 嘗試驗證圖片
        return image_file
    except (IOError, SyntaxError):
        return False
