from lib.image.is_image import is_image
from lib.image.vision_describe import vision_describe

import os

import uuid

import shutil

from lib.image.sam.init_sam import init_sam
from lib.image.sam.load_image import load_image

# 設定模型
OUTPUT_DIR = "/data/output_segments"

def process_image(file_path, chunk_config = None):
  documents = []
  image_file = is_image(file_path)
  
  if image_file is not False:
    document = vision_describe(file_path)
    # print(document)
    documents.append(document)

  IMAGE_SEGMENT_SIZE_THRESHOLD = int(os.getenv('SAM_IMAGE_SEGMENT_SIZE_THRESHOLD', 1024))
  if chunk_config and 'SAM_IMAGE_SEGMENT_SIZE_THRESHOLD' in chunk_config:
      IMAGE_SEGMENT_SIZE_THRESHOLD = int(chunk_config['SAM_IMAGE_SEGMENT_SIZE_THRESHOLD'])

  image = load_image(file_path)
  if image.shape[0] > IMAGE_SEGMENT_SIZE_THRESHOLD or image.shape[1] > IMAGE_SEGMENT_SIZE_THRESHOLD:
      mask_generator = init_sam()
      masks = mask_generator.generate(image)
      
      segment_images_output_dir = os.path.join(OUTPUT_DIR,uuid.uuid4().hex)
      # print(segment_images_output_dir)

      image_list = save_segments(image, masks, segment_images_output_dir)
      # print(image_list)

      for image_path in image_list:
        document = vision_describe(image_path)
        # print(document)
        documents.append(document)

      # print('Segment is successfully. Remove output dir: ' + segment_images_output_dir)
      shutil.rmtree(segment_images_output_dir, ignore_errors=True)
      # return image_list
      
  
  return documents