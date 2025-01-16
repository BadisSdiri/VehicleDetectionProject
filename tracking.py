import cv2
import math

vehicle_id = 0

def calculate_center(x, y, w, h):
    """Calculate the center of a rectangle."""
    return x + w // 2, y + h // 2

def calculate_speed(prev_center, curr_center, frame_rate, pixels_per_meter):
    """Calculate speed in km/h."""
    dx = curr_center[0] - prev_center[0]
    dy = curr_center[1] - prev_center[1]
    distance = math.sqrt(dx**2 + dy**2)  # Euclidean distance in pixels
    speed_pixels_per_frame = distance
    speed_meters_per_second = (speed_pixels_per_frame * frame_rate) / pixels_per_meter
    speed_kmh = speed_meters_per_second * 3.6  # Convert m/s to km/h
    return speed_kmh

def track_vehicles(contours, trackers, line_up, line_down, offset, min_width, min_height, frame_rate, pixels_per_meter, frame, frame_width):
    """
    Track vehicles, count them as they cross lines, and calculate their speed.
    """
    global vehicle_id
    vehicle_count_up = 0
    vehicle_count_down = 0
    updated_trackers = []

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w >= min_width and h >= min_height:
            center = calculate_center(x, y, w, h)

            # Match with existing trackers
            matched = False
            for tracker in trackers:
                if abs(center[0] - tracker['center'][0]) < 50 and abs(center[1] - tracker['center'][1]) < 50:
                    matched = True
                    speed = calculate_speed(tracker['center'], center, frame_rate, pixels_per_meter)
                    tracker['speed'] = speed
                    tracker['center'] = center
                    tracker['frames'] += 1

                    # Count "up" crossings
                    if not tracker.get("crossed_up") and center[1] < line_up - offset:
                        tracker["crossed_up"] = True
                        vehicle_count_up += 1

                    # Count "down" crossings
                    elif not tracker.get("crossed_down") and center[1] > line_down + offset:
                        tracker["crossed_down"] = True
                        vehicle_count_down += 1

                    # Speed capture
                    if speed > 110:
                        cv2.imwrite(f"captured/speeding_{tracker['id']}.png", frame[y:y + h, x:x + w])

            # Add new tracker if no match
            if not matched:
                updated_trackers.append({
                    'id': vehicle_id,
                    'center': center,
                    'speed': 0,
                    'frames': 1,
                    'crossed_up': False,
                    'crossed_down': False,
                })
                vehicle_id += 1

    trackers.extend(updated_trackers)
    return vehicle_count_up, vehicle_count_down, trackers
