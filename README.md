# VisionX — simple and professional (Real-Time Objetcs Detection)

Real-Time Object Detection system built using Python, OpenCV and YOLO.

The application can detect objects from a webcam, image or video in real time.

---

## Features

- Real-time object detection
- YOLO-based detection
- OpenCV webcam integration
- Multiple webcam selection
- FPS counter
- Adjustable confidence threshold
- Object counting
- Image detection
- Video detection
- Screenshot capture
- Detection logging
- Annotated image/video output

---

## Tech Stack

- Python
- OpenCV
- Ultralytics YOLO
- NumPy

---

## Project Structure

```text
Real-Time-Object-Detection/
│
├── models/
├── src/
│   ├── main.py
│   ├── detector.py
│   ├── camera.py
│   ├── config.py
│   └── utils.py
│
├── input/
│   ├── images/
│   └── videos/
│
├── output/
│   ├── images/
│   ├── videos/
│   └── screenshots/
│
├── logs/
├── test/
│
├── requirements.txt
├── README.md
└── .gitignore