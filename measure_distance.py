# measure_distance.py

import cv2

# Load the video frame
frame = cv2.imread("videos/videoframe.png")  # Replace with a specific frame from your video

# Define the two points to measure the distance
x1, y1 = 100, 200  # Replace with the coordinates of the first point
x2, y2 = 300, 200  # Replace with the coordinates of the second point

# Draw points and line for visual reference
cv2.circle(frame, (x1, y1), 5, (0, 255, 0), -1)  # Point 1
cv2.circle(frame, (x2, y2), 5, (0, 255, 0), -1)  # Point 2
cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)  # Line between points

# Display the frame to confirm the points
cv2.imshow("Measure Distance", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Calculate pixel distance
pixel_distance = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
print("Pixel Distance:", pixel_distance)

# Example: Real-world distance in meters (replace with your known value)
real_world_distance_in_meters = 3.5  # Example for lane width
PIXELS_PER_METER = pixel_distance / real_world_distance_in_meters
print("PIXELS_PER_METER:", PIXELS_PER_METER)
