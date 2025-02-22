def analyze_traffic(tracked_objects):
    left_count, right_count = 0, 0

    for obj in tracked_objects:
        x, _, w, _ = obj.to_tlbr()
        if x + w/2 < 640:
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
