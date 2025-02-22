import cv2
import numpy as np
from deep_sort_realtime.deepsort_tracker import DeepSort

class Tracker:
    def __init__(self):
        self.tracker = DeepSort(max_age=30)

    def update(self, detections, frame):
        """Update Deep SORT tracker with valid detections."""
        formatted_detections = []

        for det in detections:
            x1, y1, x2, y2, conf, cls = det
            if x1 >= 0 and y1 >= 0 and x2 > x1 and y2 > y1:
                formatted_detections.append([[x1, y1, x2, y2], conf, cls])

        if not formatted_detections:
            return []

        return self.tracker.update_tracks(formatted_detections, frame=frame)
