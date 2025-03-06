from lib.embedding.is_image import is_image
from lib.embedding.vision_describe import vision_describe

def file_to_document(document, file):
  if document:
     return document

  # ======================

  image_file = False
  if not document and file is not None:
      image_file = is_image(file)
  
      if image_file is not False:
          document = vision_describe(image_file)

  return document