from detectron2.utils.logger import setup_logger
setup_logger()

# import some common libraries
import numpy as np
import cv2
import json

# import some common detectron2 utilities
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg

class Predictor:
    def __init__(self):
        cfg = get_cfg()
        cfg.MODEL.DEVICE = "cpu"
        cfg.merge_from_file("detectron2/configs/COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
        cfg.MODEL.ROI_HEADS.NUM_CLASSES = 1
        cfg.MODEL.WEIGHTS = "predict/model/stain.pth" # 여기부분은 본인의 model이저장된 경로로 수정해줍니다.
        cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.6  # set the testing threshold for this model
        cfg.DATASETS.TEST = ("Stain",)
        self.predictor = DefaultPredictor(cfg)

    def predict(self, img):
        np_array = np.frombuffer(img.read(), dtype=np.uint8)
        # im = cv2.imdecode(np_array, -1)
        # np_array = np.frombuffer(byte, dtype=np.uint8)
        im = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
        
        outputs = self.predictor(im)
        instances = outputs["instances"]

        hasStain = False

        for i in range(len(instances)):
            score = instances.scores[i]

            if score >= 0.75:
                hasStain = True
                break

        dict = {'hasStain': hasStain}

        return dict