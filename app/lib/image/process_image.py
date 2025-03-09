from .is_image import is_image
from .vision_describe import vision_describe

import os

import uuid

import shutil

from .sam.init_sam import init_sam
from .sam.load_image import load_image
from .sam.save_segments import save_segments

# 設定模型
OUTPUT_DIR = "/data/output_segments"

def process_image(file_path, index_config = {}):
  documents = []
  image_file = is_image(file_path)
  
  if image_file is not False:
    document = vision_describe(file_path)
    # print(document)
    documents.append(document)

  IMAGE_SEGMENT_SIZE_THRESHOLD = int(os.getenv('SAM_IMAGE_SEGMENT_SIZE_THRESHOLD', 1024))
  if index_config and 'SAM_IMAGE_SEGMENT_SIZE_THRESHOLD' in index_config:
      IMAGE_SEGMENT_SIZE_THRESHOLD = int(index_config['SAM_IMAGE_SEGMENT_SIZE_THRESHOLD'])

  image = load_image(file_path)
  if image.shape[0] > IMAGE_SEGMENT_SIZE_THRESHOLD or image.shape[1] > IMAGE_SEGMENT_SIZE_THRESHOLD:
      mask_generator = init_sam()

      print('Analysing image...')
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