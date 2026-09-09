import cv2
import logging
import time

from pathlib import Path


def setup_logging(log_file):

    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    return logging.getLogger(__name__)


class FPSCounter:

    def __init__(self):

        self.start_time = time.time()
        self.frame_count = 0
        self.fps = 0

    def update(self):

        self.frame_count += 1

        elapsed = time.time() - self.start_time

        if elapsed >= 1:

            self.fps = self.frame_count / elapsed

            self.frame_count = 0
            self.start_time = time.time()

        return self.fps


def draw_info(frame, fps, object_counts, confidence):

    # FPS
    cv2.putText(
        frame,
        f"FPS: {fps:.1f}",
        (20, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2
    )

    # Confidence
    cv2.putText(
        frame,
        f"Confidence: {confidence:.2f}",
        (20, 70),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 0),
        2
    )

    # Object counts
    y = 105

    for name, count in object_counts.items():

        text = f"{name}: {count}"

        cv2.putText(
            frame,
            text,
            (20, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (0, 255, 255),
            2
        )

        y += 30

    return frame


def save_screenshot(frame, output_dir):

    timestamp = time.strftime("%Y%m%d_%H%M%S")

    filename = output_dir / f"screenshot_{timestamp}.jpg"

    cv2.imwrite(str(filename), frame)

    return filename