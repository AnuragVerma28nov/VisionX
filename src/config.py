from pathlib import Path


# Project root
BASE_DIR = Path(__file__).resolve().parent.parent


# Directories
INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"
LOG_DIR = BASE_DIR / "logs"
MODEL_DIR = BASE_DIR / "models"


# Output directories
IMAGE_OUTPUT_DIR = OUTPUT_DIR / "images"
VIDEO_OUTPUT_DIR = OUTPUT_DIR / "videos"
SCREENSHOT_DIR = OUTPUT_DIR / "screenshots"


# Create directories if they don't exist
for directory in [
    IMAGE_OUTPUT_DIR,
    VIDEO_OUTPUT_DIR,
    SCREENSHOT_DIR,
    LOG_DIR,
]:
    directory.mkdir(parents=True, exist_ok=True)


# YOLO model
MODEL_PATH = "yolo26n.pt"


# Detection settings
CONFIDENCE_THRESHOLD = 0.50
IMAGE_SIZE = 640


# Camera settings
DEFAULT_CAMERA_INDEX = 0


# Window
WINDOW_NAME = "Real-Time Object Detection"