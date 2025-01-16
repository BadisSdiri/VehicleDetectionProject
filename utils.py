# utils.py

import cv2
import numpy as np

def initialize_background_subtractor():
    return cv2.bgsegm.createBackgroundSubtractorMOG()

def preprocess_frame(frame, kernel_size):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 5)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, kernel_size)
    dilated = cv2.dilate(blur, kernel, iterations=2)
    processed = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel)
    return processed

def draw_lines(frame, position, color=(0, 255, 255)):
    cv2.line(frame, (25, position), (1200, position), color, 3)

def calculate_center(x, y, w, h):
    return x + w // 2, y + h // 2
