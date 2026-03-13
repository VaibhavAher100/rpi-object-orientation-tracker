import cv2
import numpy as np
import time
import os
from collections import deque

from angle_filter import update_filter
from logger import log_result

# -----------------------------------------------------------------------------
# Paths — resolved from repo root regardless of where the script is called from
# -----------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIDEO_SOURCE = os.path.join(BASE_DIR, "foreground.mp4")
CASCADE_XML = os.path.join(BASE_DIR, "classifiers",
                           "pen_vertical_classifier.xml")
LOG_FILE = os.path.join(BASE_DIR, "results", "detections.csv")

# -----------------------------------------------------------------------------
# Set to True when running on RPi5 with Picamera2
# Set to False to use a video file or laptop webcam instead
# -----------------------------------------------------------------------------
USE_PICAMERA = False
WINDOW_SIZE = 5


def hough_transform(x: int, y: int, w: int, h: int, image: np.ndarray) -> float:
    """
    Apply Canny + Hough on a cropped ROI around the detected object.
    Draws the main line and angle onto the original image.
    Returns the angle in degrees, or -1.0 if no line was found.
    """
    height, width = image.shape[:2]

    if (
        x - 200 >= 0
        and y - 100 >= 0
        and x + w + 200 <= width
        and y + h + 100 <= height
    ):
        x0, y0, x1, y1 = x - 200, y - 100, x + w + 200, y + h + 100
    elif (
        x - 40 >= 0
        and y - 20 >= 0
        and x + w + 40 <= width
        and y + h + 20 <= height
    ):
        x0, y0, x1, y1 = x - 40, y - 20, x + w + 40, y + h + 20
    else:
        x0, y0 = max(x, 0), max(y, 0)
        x1, y1 = min(x + w, width), min(y + h, height)

    cropped_image = image[y0:y1, x0:x1]

    gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
    edge_image = cv2.Canny(gray, 50, 150, apertureSize=3)
    lines = cv2.HoughLines(edge_image, 1, np.pi / 180, 80)

    if lines is None:
        return -1.0

    for rho, theta in lines[0]:
        a, b = np.cos(theta), np.sin(theta)
        x0_l, y0_l = a * rho, b * rho
        x1_l = int(x0_l + 1000 * (-b))
        y1_l = int(y0_l + 1000 * (a))
        x2_l = int(x0_l - 1000 * (-b))
        y2_l = int(y0_l - 1000 * (a))

        cv2.line(cropped_image, (x1_l, y1_l), (x2_l, y2_l), (0, 0, 255), 2)

        angle_deg = theta * 180 / np.pi
        angle = angle_deg - 180 if angle_deg > 180 else angle_deg

        cv2.putText(image, f"{angle:.1f}", (10, 25),
                    cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

        return angle

    return -1.0


def run() -> None:
    """
    Main detection loop. Reads frames, detects objects, measures orientation,
    applies moving average filter, logs results to CSV.
    """
    clf = cv2.CascadeClassifier(CASCADE_XML)
    if clf.empty():
        raise RuntimeError(f"Could not load cascade: {CASCADE_XML}")

    if USE_PICAMERA:
        from picamera2 import Picamera2
        picam2 = Picamera2()
        picam2.configure(picam2.create_preview_configuration(
            main={"format": "XRGB8888", "size": (640, 480)}
        ))
        picam2.start()
        time.sleep(1)
    else:
        cap = cv2.VideoCapture(VIDEO_SOURCE)
        if not cap.isOpened():
            raise RuntimeError(f"Could not open video source: {VIDEO_SOURCE}")

    window = deque(maxlen=WINDOW_SIZE)

    cv2.namedWindow("detector", cv2.WINDOW_NORMAL)

    while True:
        if USE_PICAMERA:
            frame = picam2.capture_array()
            if frame.shape[2] == 4:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
        else:
            ret, frame = cap.read()
            if not ret:
                break

        gray = cv2.cvtColor(cv2.GaussianBlur(
            frame, (5, 5), 0), cv2.COLOR_BGR2GRAY)

        objects = clf.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(40, 40),
            flags=cv2.CASCADE_SCALE_IMAGE,
        )

        raw_angle = -1.0
        filtered_angle = -1.0
        object_count = len(objects) if objects is not None and len(
            objects) > 0 else 0

        for (x, y, w, h) in objects:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            raw_angle = hough_transform(x, y, w, h, frame)
            if raw_angle >= 0:
                filtered_angle = update_filter(window, raw_angle)

        log_result(LOG_FILE, time.time(), raw_angle,
                   filtered_angle, object_count)

        cv2.imshow("detector", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    if USE_PICAMERA:
        picam2.stop()
    else:
        cap.release()

    cv2.destroyAllWindows()


if __name__ == "__main__":
    run()
