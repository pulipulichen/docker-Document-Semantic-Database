import cv2
import os
import numpy as np


# **過濾掉小於原圖 10% 面積的 segmentation**
def save_segments(image, masks, output_dir, chunk_config=None):
    os.makedirs(output_dir, exist_ok=True)
    image_list = []

    MIN_SEGMENT_RATIO = float(os.getenv('SAM_MIN_SEGMENT_RATIO', 0.05))
    if chunk_config and 'SAM_MIN_SEGMENT_RATIO' in chunk_config:
        MIN_SEGMENT_RATIO = float(chunk_config['SAM_MIN_SEGMENT_RATIO'])

    img_h, img_w, _ = image.shape  # 取得原圖大小
    min_area = img_h * img_w * MIN_SEGMENT_RATIO  # 計算最小可接受面積

    for i, mask in enumerate(masks):
        print('Processing mask ' + str(i))
        segmentation = mask["segmentation"]
        x, y, w, h = cv2.boundingRect(segmentation.astype(np.uint8))
        if w == img_w and h == img_h:
            continue

        segment_area = w * h  # 計算 segmentation 面積
        
        # **過濾掉小於原圖 10% 面積的 segmentation**
        if segment_area >= min_area:
            sub_image = image[y:y+h, x:x+w]
            sub_image_path = os.path.join(output_dir, f"segment_{i}.png")
            cv2.imwrite(sub_image_path, cv2.cvtColor(sub_image, cv2.COLOR_RGB2BGR))
            image_list.append(sub_image_path)

    return image_list