import cv2
import os
from config import *
from preprocessing import initialize_background_subtractor, preprocess_frame
from tracking import track_vehicles
from visualization import draw_refined_lines, draw_bounding_boxes, display_count

def main():
    # Initialize video capture
    cap = cv2.VideoCapture(VIDEO_PATH)
    if not cap.isOpened():
        print("Error opening video file.")
        return

    # Ensure the "captured" folder exists
    if not os.path.exists("captured"):
        os.makedirs("captured")

    # Initialize background subtractor
    bg_subtractor = initialize_background_subtractor()
    trackers = []
    vehicle_count_up = 0
    vehicle_count_down = 0
    frame_rate = int(cap.get(cv2.CAP_PROP_FPS))

    # Define symmetrical line positions
    line_position = FRAME_HEIGHT - 150  # Base line for symmetry
    line_up = line_position - 20  # "Up" line slightly above
    line_down = line_position + 20  # "Down" line slightly below

    # Initialize video writer
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(OUTPUT_PATH, fourcc, frame_rate, (FRAME_WIDTH, FRAME_HEIGHT))

    # Processing loop
    while True:
        # Read a frame from the video
        ret, frame = cap.read()
        if not ret:
            break

        # Preprocess the frame
        resized, processed_frame = preprocess_frame(frame, bg_subtractor)
        contours, _ = cv2.findContours(processed_frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Track vehicles and count them
        count_up, count_down, trackers = track_vehicles(
            contours, trackers, line_up, line_down, OFFSET, MIN_WIDTH_RECT, MIN_HEIGHT_RECT, frame_rate, PIXELS_PER_METER, resized, FRAME_WIDTH
        )
        vehicle_count_up += count_up
        vehicle_count_down += count_down

        # Draw lines, bounding boxes, and counts
        draw_refined_lines(resized, line_up, line_down)
        draw_bounding_boxes(resized, contours, MIN_WIDTH_RECT, MIN_HEIGHT_RECT, trackers)
        display_count(resized, vehicle_count_up, vehicle_count_down)

        # Display the processed frame and save to output
        cv2.imshow("Vehicle Detection", resized)
        out.write(resized)

        # Break loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
