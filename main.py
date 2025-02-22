import cv2
from utils import load_yolo_model, preprocess_frame
from tracker import Tracker
from traffic_flow import analyze_traffic
from visualization import draw_detections
from reporting import save_report
import config

# Load YOLO Model
print("🔄 Loading YOLO Model...")
model = load_yolo_model()
print("✅ YOLO Model Loaded Successfully!")

tracker = Tracker()
frame_number = 0

cap = cv2.VideoCapture(config.INPUT_VIDEO_PATH)
if not cap.isOpened():
    print("❌ Error: Unable to open input video file.")
    exit(1)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(config.PROCESSED_VIDEO_PATH, fourcc, 30.0, (int(cap.get(3)), int(cap.get(4))))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_number += 1
    detections = preprocess_frame(frame, model)
    tracked_objects = tracker.update(detections, frame)
    frame, total_left_ROI, total_right_ROI, traffic_status = draw_detections(frame, tracked_objects, analyze_traffic(tracked_objects), frame_number)

    out.write(frame)
    save_report(tracked_objects, frame_number, total_left_ROI, total_right_ROI, traffic_status, config.OUTPUT_CSV_PATH)

cap.release()
out.release()
cv2.destroyAllWindows()
