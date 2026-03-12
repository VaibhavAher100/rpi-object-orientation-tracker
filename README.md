# Embedded Object Orientation Tracker

Real-time object detection and orientation measurement 
on Raspberry Pi 5. Runs without a GPU on 1GB RAM.

---

## Hardware

- Raspberry Pi 5 (1GB)
- Raspberry Pi HQ Camera Module
- GPIO button (pin 6) for clean exit

*[Photo of hardware setup — add after RPi5 session]*

---

## Pipeline
```
Camera → Grayscale → GaussianBlur → Haar Detection
→ Crop ROI → Canny Edge Detection → Hough Transform  
→ Moving Average Filter → CSV Log + Live Display
```

*[Screenshot of annotated live feed — add after RPi5 session]*

---

## Results

*[Angle trace plot — add after RPi5 session]*

---

## Usage
```bash
python src/detector.py \
  --classifier classifiers/pen_vertical.xml \
  --output results/session1.csv \
  --filter-window 5
```

---

## Project Structure
```
src/detector.py          — main pipeline
src/angle_filter.py      — moving average filter
src/logger.py            — CSV logging
src/visualize_results.py — plot angle trace from CSV
classifiers/             — Haar XML files (see classifiers/README.md)
results/                 — CSV logs and output plots
docs/pipeline.md         — detailed pipeline documentation
```

---

## Based on

FAU Erlangen-Nürnberg BiViP Lab,
extended with:

- Moving average filter on angle output
- CSV timestamped logging
- CLI configuration
- Results visualization

---

## Requirements
```bash
pip install -r requirements.txt
```

Designed for Raspberry Pi OS. 
For laptop testing, replace Picamera2 with cv2.VideoCapture(0).