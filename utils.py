import cv2
import numpy as np
from ultralytics import YOLO
import config  # Import configuration


def load_yolo_model():
    """Load YOLOv11 model using Ultralytics."""
    model = YOLO(config.YOLO_MODEL_TYPE)  # Load YOLO model
    return model


def preprocess_frame(frame, model):
    """Run YOLO model on a frame and extract vehicle detections."""
    results = model(frame)  # Perform detection
    detections = []

    for result in results:
        boxes = result.boxes  # Extract bounding boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()  # Get bounding box coordinates
            conf = box.conf[0].item()  # Confidence score
            cls = int(box.cls[0].item())  # Class ID

            if conf > config.CONFIDENCE_THRESHOLD and cls == 2:  # Vehicle class
                detections.append([x1, y1, x2, y2, conf, cls])  # Include class_id!

    return detections
