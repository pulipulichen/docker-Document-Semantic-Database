from segment_anything import sam_model_registry, SamAutomaticMaskGenerator
import torch
import os

from .download_checkpoint import download_checkpoint

MODEL_TYPE = os.getenv("SAM_MODEL_TYPE", "vit_h")
CHECKPOINT_PATH = os.path.join("/data/models/", os.getenv("SAM_CHECKPOINT_NAME", "sam_vit_h.pth"))

MASK_GENERATOR = None
# 初始化 Segment Anything 模型
def init_sam():
    global MASK_GENERATOR
    if MASK_GENERATOR is not None:
        return MASK_GENERATOR

    print('Download checkpoint model...')
    download_checkpoint()

    print('Load the model...')
    sam = sam_model_registry[MODEL_TYPE](checkpoint=CHECKPOINT_PATH)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print('Move to device...')
    sam.to(device=device)

    print('Create automatic mask generator...')
    MASK_GENERATOR = SamAutomaticMaskGenerator(sam)
    return MASK_GENERATOR
