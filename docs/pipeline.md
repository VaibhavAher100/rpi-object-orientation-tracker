# Pipeline Documentation

## Overview

This pipeline detects objects in a live camera feed and 
measures their orientation angle in real time.

## Stage by Stage

### 1. Camera Input
Picamera2 captures frames at 640x480.
Each frame is a NumPy array (XRGB8888 format).

### 2. Preprocessing
- Convert to grayscale (cv2.cvtColor)
- Apply Gaussian blur (11x11 kernel, sigma=20)
  to reduce noise before detection

### 3. Object Detection
- Haar cascade classifier (pen_vertical.xml)
- detectMultiScale parameters:
  - scaleFactor: 1.7
  - minNeighbors: 25
  - minSize: (25, 80)
- Returns bounding box(es): (x, y, w, h)

### 4. ROI Crop
- Crop the detected bounding box from the frame
- Enlarge the crop by a margin to improve Hough accuracy
  (200px / 100px in x/y, fallback to 40px / 20px)
- Boundary check to avoid going outside frame edges

### 5. Edge Detection
- Apply Canny on the cropped grayscale region
  - Tlow = 50
  - Thigh = 150
  - apertureSize = 3

### 6. Hough Transform
- cv2.HoughLines on the edge image
- Returns lines in (rho, theta) format
- Extract dominant line

### 7. Angle Computation
- Compute angle from theta
- Normalize to 0-180 degree range

### 8. Moving Average Filter
- Maintain a rolling window of last N angle measurements
- Return mean of the window
- Reduces frame-to-frame noise

### 9. Logging
- Write to CSV: timestamp, raw_angle, filtered_angle, 
  object_count
- One row per frame

### 10. Display
- Draw bounding box on original frame (cv2.rectangle)
- Overlay filtered angle as text (cv2.putText)
- Show live feed (cv2.imshow)

## Parameters (CLI configurable)
- --classifier: path to XML file
- --output: path to CSV log file
- --filter-window: moving average window size (default 5)
- --width: frame width (default 640)
- --height: frame height (default 480)