
import cv2
import numpy as np
from ultralytics import YOLO
import config  

def load_yolo_model():
    """Load YOLO model using Ultralytics."""
    model = YOLO(config.YOLO_MODEL_TYPE)
    return model

def preprocess_frame(frame, model):
    """Run YOLO model on a frame and extract vehicle detections.

    Returns detections as [x1, y1, x2, y2, conf, cls].
    Accepts any class present in config.CLASS_NAMES mapping.
    """
    results = model(frame) 
    detections = []

    for result in results:
        boxes = getattr(result, "boxes", [])
        for box in boxes:
            
            try:
                coords = box.xyxy[0].tolist()
            except Exception:
                
                coords = [float(box[0]), float(box[1]), float(box[2]), float(box[3])]

            x1, y1, x2, y2 = [float(v) for v in coords]
            
            try:
                conf = float(box.conf[0].item())
            except Exception:
                conf = float(box.conf)

            try:
                cls = int(box.cls[0].item())
            except Exception:
                cls = int(box.cls)

           
            if conf > config.CONFIDENCE_THRESHOLD and cls in config.CLASS_NAMES:
                detections.append([x1, y1, x2, y2, conf, cls])

    return detections
