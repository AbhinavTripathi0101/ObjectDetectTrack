
def analyze_traffic(tracked_objects, frame_width):
    """
    Analyze traffic by separating tracked objects into left/right based on box center.
    frame_width: width of the frame in pixels (use frame.shape[1] when calling).
    """
    left_count, right_count = 0, 0

    for obj in tracked_objects:
        
        x1, y1, x2, y2 = obj.to_tlbr()
        center_x = (x1 + x2) / 2.0
        if center_x < (frame_width / 2.0):
            left_count += 1
        else:
            right_count += 1

    total = left_count + right_count
    if total < 5:
        return "Light Traffic"
    elif total < 10:
        return "Moderate Traffic"
    else:
        return "Heavy Traffic"
