import pandas as pd
import config

def save_report(tracked_objects, frame_number, total_left_ROI, total_right_ROI, traffic_status, filename=config.OUTPUT_CSV_PATH, frame_width=None):
    """Save tracking results with ROI analysis to CSV.

    frame_width: optional, used to compute left/right zone consistently.
    """
    data = []

    for obj in tracked_objects:
        x1, y1, x2, y2 = obj.to_tlbr()
        object_id = getattr(obj, "track_id", None)
        class_name = config.CLASS_NAMES.get(getattr(obj, "det_class", None), "Unknown")

        center_x = (x1 + x2) / 2.0
        threshold = (frame_width / 2.0) if frame_width is not None else 640
        zone = "Left Lane" if center_x < threshold else "Right Lane"

        data.append([frame_number, object_id, class_name, zone, total_left_ROI, total_right_ROI, traffic_status])

    df = pd.DataFrame(data, columns=["Frame Number", "Object ID", "Object Class", "Zone", "Total Left ROI", "Total Right ROI", "Traffic Status"])
    df.to_csv(filename, mode='a', index=False, header=not config.FILE_EXISTS)
    config.FILE_EXISTS = True
