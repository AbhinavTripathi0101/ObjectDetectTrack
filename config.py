import os

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")

# Ensure the outputs folder exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

INPUT_VIDEO_PATH = os.path.join(BASE_DIR, "data", "traffic_video.mp4")
OUTPUT_CSV_PATH = os.path.join(OUTPUT_DIR, "output.csv")
OUTPUT_REPORT_PATH = os.path.join(OUTPUT_DIR, "report.txt")
PROCESSED_VIDEO_PATH = os.path.join(OUTPUT_DIR, "processed_video.mp4")

# YOLO Model Configuration
YOLO_MODEL_TYPE = "yolo11n.pt"  # Change if using a different model
CONFIDENCE_THRESHOLD = 0.4  # Minimum confidence for object detection

# Class Names for YOLO vehicle detection
CLASS_NAMES = {2: "Car", 3: "Motorcycle", 5: "Bus", 7: "Truck"}

# Flag to prevent overwriting CSV file header
FILE_EXISTS = False
