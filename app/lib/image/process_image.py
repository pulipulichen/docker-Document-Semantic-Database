from lib.image.is_image import is_image
from lib.image.vision_describe import vision_describe

def process_image(file_path, file):
  documents = []
  image_file = is_image(file_path)
  
  if image_file is not False:
    document = vision_describe(file_path)
    print(document)
    documents.append(document)

  return documents