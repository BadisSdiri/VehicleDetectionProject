# visualization.py

import cv2
from config import FONT
from tracking import calculate_center  



# visualization.py

# visualization.py

def draw_refined_lines(frame, line_up, line_down):
    """Draw symmetric lines for up and down directions with labels."""
    # "Up" line (blue)
    cv2.line(frame, (50, line_up), (frame.shape[1] - 50, line_up), (255, 0, 0), 2)
    cv2.putText(frame, "UP", (10, line_up - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

    # "Down" line (green)
    cv2.line(frame, (50, line_down), (frame.shape[1] - 50, line_down), (0, 255, 0), 2)
    cv2.putText(frame, "DOWN", (10, line_down + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

def draw_bounding_boxes(frame, contours, min_width, min_height, trackers):
    """Draw bounding boxes and display speeds."""
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w >= min_width and h >= min_height:
            center = calculate_center(x, y, w, h)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            for tracker in trackers:
                if tracker['center'] == center:
                    cv2.putText(frame, f"{tracker['speed']:.1f} km/h", (x, y - 10), FONT, 0.5, (0, 255, 255), 2)


# visualization.py

def display_count(frame, count_up, count_down):
    """Display the vehicle counts on the frame."""
    cv2.putText(frame, f"Going Up: {count_up}", (50, 50), FONT, 1, (0, 255, 0), 2)
    cv2.putText(frame, f"Going Down: {count_down}", (50, 100), FONT, 1, (0, 0, 255), 2)
