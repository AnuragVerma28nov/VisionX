from collections import Counter

from ultralytics import YOLO


class ObjectDetector:

    def __init__(
        self,
        model_path,
        confidence=0.50,
        image_size=640
    ):
        self.model = YOLO(model_path)

        self.confidence = confidence
        self.image_size = image_size

    def detect(self, frame):

        results = self.model.predict(
            source=frame,
            conf=self.confidence,
            imgsz=self.image_size,
            verbose=False
        )

        return results[0]

    def get_object_counts(self, result):

        counts = Counter()

        if result.boxes is None:
            return counts

        for class_id in result.boxes.cls:

            class_id = int(class_id)

            class_name = result.names[class_id]

            counts[class_name] += 1

        return counts

    def draw_detections(self, result):

        return result.plot()