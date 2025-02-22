import cv2
import config

object_tracks = {}

def draw_detections(frame, tracked_objects, traffic_state, frame_number):
    """Draw bounding boxes and display tracking details."""
    num_detected_objects = len(tracked_objects)
    total_left_ROI, total_right_ROI = 0, 0  # Counters for each ROI

    for obj in tracked_objects:
        x1, y1, x2, y2 = map(int, obj.to_tlbr())
        object_id = obj.track_id
        class_id = obj.det_class if obj.det_class in config.CLASS_NAMES else "Unknown"
        class_name = config.CLASS_NAMES.get(class_id, "Unknown")

        # **Reduce Bounding Box Size**
        scale_factor = 0.90  # Reduce size by 10%
        new_width = int((x2 - x1) * scale_factor)
        new_height = int((y2 - y1) * scale_factor)
        x1 = x1 + int((x2 - x1 - new_width) / 2)  # Centering the box
        y1 = y1 + int((y2 - y1 - new_height) / 2)
        x2 = x1 + new_width
        y2 = y1 + new_height

        # **Determine Movement Direction**
        if object_id in object_tracks:
            prev_x = object_tracks[object_id]
            direction = "Right" if x1 > prev_x else "Left"
        else:
            direction = "Unknown"

        object_tracks[object_id] = x1

        # **Determine ROI Zone**
        if x1 < frame.shape[1] // 2:
            total_left_ROI += 1
        else:
            total_right_ROI += 1

        # Draw bounding box with reduced size
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, f"ID {object_id} - {class_name}", (x1, y1 - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        cv2.putText(frame, f"Direction: {direction}", (x1, y2 + 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)

    # **Traffic Status Based on ROI Counts**
    traffic_status = "Heavy" if num_detected_objects > 10 else "Moderate" if num_detected_objects > 5 else "Light"

    # Display ROI Counts & Traffic Status
    cv2.putText(frame, f"Traffic: {traffic_status} | Vehicles: {num_detected_objects}",
                (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(frame, f"Left ROI: {total_left_ROI} | Right ROI: {total_right_ROI}",
                (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 165, 0), 2)

    return frame, total_left_ROI, total_right_ROI, traffic_status
