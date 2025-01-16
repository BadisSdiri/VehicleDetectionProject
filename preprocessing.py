# preprocessing.py

import cv2
import numpy as np
from config import FRAME_WIDTH, FRAME_HEIGHT

def initialize_background_subtractor():
    """Initialize the background subtractor."""
    return cv2.bgsegm.createBackgroundSubtractorMOG()

def preprocess_frame(frame, bg_subtractor):
    """Preprocess the frame for object detection."""
    resized = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 5)
    fg_mask = bg_subtractor.apply(blurred)
    
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    dilated = cv2.dilate(fg_mask, kernel, iterations=2)
    processed = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel)
    return resized, processed
