# config.py

import cv2


VIDEO_PATH = "videos/video.mp4"
OUTPUT_PATH = "outputs/processed_videos.avi"

FRAME_WIDTH = 1280
FRAME_HEIGHT = 720
LINE_POSITION = FRAME_HEIGHT // 2 
OFFSET = 6 


MIN_WIDTH_RECT = 80
MIN_HEIGHT_RECT = 80

PIXELS_PER_METER = 16.33  

# Visualization
FONT = cv2.FONT_HERSHEY_SIMPLEX
