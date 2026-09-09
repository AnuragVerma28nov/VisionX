## ARCHITECTURE

```
                    ┌─────────────────┐
                    │    main.py      │
                    │ Application     │
                    │ Controller      │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              ↓              ↓              ↓
       ┌────────────┐ ┌────────────┐ ┌────────────┐
       │  camera.py │ │ detector.py│ │  utils.py  │
       │            │ │            │ │            │
       │ OpenCV     │ │ YOLO       │ │ FPS        │
       │ Webcam     │ │ Detection  │ │ Screenshot │
       │ Video      │ │ Counting   │ │ Logging    │
       └────────────┘ └────────────┘ └────────────┘
              │              │              │
              └──────────────┼──────────────┘
                             ↓
                    ┌─────────────────┐
                    │     Output      │
                    ├─────────────────┤
                    │ Bounding Boxes  │
                    │ Object Counts   │
                    │ FPS             │
                    │ Screenshots     │
                    │ Videos          │
                    │ Logs            │
                    └─────────────────┘

```