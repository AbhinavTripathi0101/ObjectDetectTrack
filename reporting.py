import pandas as pd
import config

def save_report(tracked_objects, frame_number, total_left_ROI, total_right_ROI, traffic_status, filename=config.OUTPUT_CSV_PATH):
    """Save tracking results with ROI analysis to CSV."""
    data = []

    for obj in tracked_objects:
        x1, y1, x2, y2 = obj.to_tlbr()
        object_id = obj.track_id
        class_name = config.CLASS_NAMES.get(obj.det_class, "Unknown")
        zone = "Left Lane" if x1 < 640 else "Right Lane"

        data.append([frame_number, object_id, class_name, zone, total_left_ROI, total_right_ROI, traffic_status])

    df = pd.DataFrame(data, columns=["Frame Number", "Object ID", "Object Class", "Zone", "Total Left ROI", "Total Right ROI", "Traffic Status"])
    df.to_csv(filename, mode='a', index=False, header=not config.FILE_EXISTS)
    config.FILE_EXISTS = True
