# Pipeline Documentation

## Overview
This pipeline detects objects in a live camera feed and
measures their orientation angle in real time.

## Stage by Stage

### 1. Camera Input
Picamera2 captures frames at 640x480.
Each frame is a NumPy array (XRGB8888 format).
On laptop, cv2.VideoCapture is used instead — set USE_PICAMERA = False
in detector.py or pass --no-picamera via CLI.

### 2. Preprocessing
- Convert to grayscale (cv2.cvtColor)
- Apply Gaussian blur (5x5 kernel, sigma=0)
  to reduce noise before detection

### 3. Object Detection
- Haar cascade classifier (pen_vertical_classifier.xml)
- detectMultiScale parameters:
  - scaleFactor: 1.1
  - minNeighbors: 5
  - minSize: (40, 40)
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
- Maintain a rolling window of last N angle measurements (default: 5)
- Return mean of the window
- Reduces frame-to-frame noise

### 9. Logging
- Write to CSV: timestamp, raw_angle, filtered_angle, object_count
- One row per frame
- File created with header on first write

### 10. Display
- Draw bounding box on original frame (cv2.rectangle)
- Overlay angle as text (cv2.putText)
- Show live feed (cv2.imshow)

## Parameters (CLI configurable)
- --cascade: path to classifier XML file (default: classifiers/pen_vertical_classifier.xml)
- --source: path to video file or camera index (default: 0)
- --log: path to CSV log file (default: results/detections.csv)
- --window: moving average window size (default: 5)