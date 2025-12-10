
import cv2
import config


object_tracks = {}

def draw_detections(frame, tracked_objects, traffic_state, frame_number):
    """Draw bounding boxes and display tracking details.

    Improvements:
    - Direction decided using object center (not x1) and smoothed by a threshold.
    - Zone (Left/Right) decided using raw box center BEFORE resizing for display.
    - Per-object state stored as dict to avoid flipping due to small jitter.
    """
    num_detected_objects = len(tracked_objects)
    total_left_ROI, total_right_ROI = 0, 0  
    frame_width = frame.shape[1]

    
    MOVEMENT_THRESHOLD = 3

    for obj in tracked_objects:
        
        x1f, y1f, x2f, y2f = obj.to_tlbr()
        
        center_x = (x1f + x2f) / 2.0
        center_y = (y1f + y2f) / 2.0

        
        x1, y1, x2, y2 = map(int, (x1f, y1f, x2f, y2f))
        object_id = getattr(obj, "track_id", None)

        # Safely fetch class id/name
        class_id = getattr(obj, "det_class", None)
        if class_id is None:
            class_id = getattr(obj, "detector_class", None)
        class_name = config.CLASS_NAMES.get(class_id, "Unknown")

       
        zone = "Left Lane" if center_x < (frame_width / 2.0) else "Right Lane"

      
        if zone == "Left Lane":
            total_left_ROI += 1
        else:
            total_right_ROI += 1

        
        prev = object_tracks.get(object_id, None)

        if prev is None:
            
            direction = "Unknown"
            object_tracks[object_id] = {
                "center_x": center_x,
                "last_direction": direction,
                "last_zone": zone
            }
        else:
            prev_center = prev.get("center_x", center_x)
            dx = center_x - prev_center

            
            if abs(dx) >= MOVEMENT_THRESHOLD:
                direction = "Right" if dx > 0 else "Left"
                prev["last_direction"] = direction
            else:
                
                direction = prev.get("last_direction", "Unknown")

            
            prev["center_x"] = center_x
            prev["last_zone"] = zone
            object_tracks[object_id] = prev

        
        scale_factor = 0.90  
        width = x2 - x1
        height = y2 - y1
        if width > 4 and height > 4:
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)
            x1_draw = x1 + int((width - new_width) / 2)
            y1_draw = y1 + int((height - new_height) / 2)
            x2_draw = x1_draw + new_width
            y2_draw = y1_draw + new_height
        else:
            
            x1_draw, y1_draw, x2_draw, y2_draw = x1, y1, x2, y2

        
        cv2.rectangle(frame, (x1_draw, y1_draw), (x2_draw, y2_draw), (0, 255, 0), 2)
        cv2.putText(frame, f"ID {object_id} - {class_name}", (x1_draw, max(5, y1_draw - 20)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        cv2.putText(frame, f"{zone} | Dir: {direction}", (x1_draw, min(frame.shape[0] - 5, y2_draw + 20)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)

    
    traffic_status = "Heavy" if num_detected_objects > 10 else "Moderate" if num_detected_objects > 5 else "Light"

    
    cv2.putText(frame, f"Traffic: {traffic_status} | Vehicles: {num_detected_objects}",
                (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(frame, f"Left ROI: {total_left_ROI} | Right ROI: {total_right_ROI}",
                (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 165, 0), 2)

    return frame, total_left_ROI, total_right_ROI, traffic_status
