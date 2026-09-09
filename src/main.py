import argparse
import cv2
import logging
import time

from config import (
    DEFAULT_CAMERA_INDEX,
    MODEL_PATH,
    CONFIDENCE_THRESHOLD,
    IMAGE_SIZE,
    WINDOW_NAME,
    IMAGE_OUTPUT_DIR,
    VIDEO_OUTPUT_DIR,
    SCREENSHOT_DIR,
    LOG_DIR,
)

from detector import ObjectDetector
from camera import Camera, find_available_cameras

from utils import (
    FPSCounter,
    draw_info,
    save_screenshot,
    setup_logging,
)


def detect_webcam(camera_index, confidence):

    logger = setup_logging(
        LOG_DIR / "detection.log"
    )

    logger.info(
        f"Starting webcam detection | "
        f"Camera={camera_index} | "
        f"Confidence={confidence}"
    )

    camera = Camera(camera_index)

    if not camera.is_opened():

        print(
            f"Error: Could not open camera "
            f"{camera_index}"
        )

        return

    detector = ObjectDetector(
        MODEL_PATH,
        confidence,
        IMAGE_SIZE
    )

    fps_counter = FPSCounter()

    print("\nReal-Time Object Detection")
    print("---------------------------")
    print("Q → Quit")
    print("S → Screenshot")
    print("C → Increase confidence")
    print("X → Decrease confidence")
    print()

    while True:

        ret, frame = camera.read()

        if not ret:

            print("Error reading camera frame.")

            break

        # Detection
        result = detector.detect(frame)

        # Annotated frame
        output = detector.draw_detections(result)

        # Object count
        object_counts = detector.get_object_counts(result)

        # FPS
        fps = fps_counter.update()

        # Draw information
        output = draw_info(
            output,
            fps,
            object_counts,
            confidence
        )

        # Display
        cv2.imshow(
            WINDOW_NAME,
            output
        )

        key = cv2.waitKey(1) & 0xFF

        # Quit
        if key == ord("q"):
            break

        # Screenshot
        elif key == ord("s"):

            path = save_screenshot(
                output,
                SCREENSHOT_DIR
            )

            print(
                f"Screenshot saved: {path}"
            )

            logger.info(
                f"Screenshot saved: {path}"
            )

        # Increase confidence
        elif key == ord("c"):

            confidence = min(
                confidence + 0.05,
                0.95
            )

            detector.confidence = confidence

            print(
                f"Confidence: {confidence:.2f}"
            )

        # Decrease confidence
        elif key == ord("x"):

            confidence = max(
                confidence - 0.05,
                0.05
            )

            detector.confidence = confidence

            print(
                f"Confidence: {confidence:.2f}"
            )

        # Log detection
        if object_counts:

            logger.info(
                f"Objects detected: "
                f"{dict(object_counts)}"
            )

    camera.release()

    cv2.destroyAllWindows()

    logger.info("Webcam detection stopped.")


def detect_image(image_path, confidence):

    logger = setup_logging(
        LOG_DIR / "detection.log"
    )

    detector = ObjectDetector(
        MODEL_PATH,
        confidence,
        IMAGE_SIZE
    )

    image = cv2.imread(str(image_path))

    if image is None:

        print(
            f"Error: Could not read image: "
            f"{image_path}"
        )

        return

    result = detector.detect(image)

    output = detector.draw_detections(result)

    object_counts = detector.get_object_counts(
        result
    )

    output = draw_info(
        output,
        0,
        object_counts,
        confidence
    )

    output_path = (
        IMAGE_OUTPUT_DIR /
        f"detected_{image_path.name}"
    )

    cv2.imwrite(
        str(output_path),
        output
    )

    print(f"\nOutput saved: {output_path}")

    print("\nObjects detected:")

    for name, count in object_counts.items():

        print(f"  {name}: {count}")

    logger.info(
        f"Image processed: {image_path} | "
        f"Objects: {dict(object_counts)}"
    )

    cv2.imshow(
        "Image Detection",
        output
    )

    cv2.waitKey(0)

    cv2.destroyAllWindows()


def detect_video(video_path, confidence):

    logger = setup_logging(
        LOG_DIR / "detection.log"
    )

    detector = ObjectDetector(
        MODEL_PATH,
        confidence,
        IMAGE_SIZE
    )

    cap = cv2.VideoCapture(
        str(video_path)
    )

    if not cap.isOpened():

        print(
            f"Error: Could not open video: "
            f"{video_path}"
        )

        return

    width = int(
        cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    )

    height = int(
        cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    )

    fps = cap.get(
        cv2.CAP_PROP_FPS
    )

    if fps <= 0:
        fps = 30

    output_path = (
        VIDEO_OUTPUT_DIR /
        f"detected_{video_path.stem}.mp4"
    )

    fourcc = cv2.VideoWriter_fourcc(
        *"mp4v"
    )

    writer = cv2.VideoWriter(
        str(output_path),
        fourcc,
        fps,
        (width, height)
    )

    print("\nProcessing video...")
    print("Press Q to stop.")

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        result = detector.detect(frame)

        output = detector.draw_detections(
            result
        )

        object_counts = (
            detector.get_object_counts(result)
        )

        output = draw_info(
            output,
            fps,
            object_counts,
            confidence
        )

        writer.write(output)

        cv2.imshow(
            "Video Detection",
            output
        )

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()

    writer.release()

    cv2.destroyAllWindows()

    print(
        f"\nOutput saved: {output_path}"
    )

    logger.info(
        f"Video processed: {video_path}"
    )


def main():

    parser = argparse.ArgumentParser(
        description="Real-Time Object Detection"
    )

    parser.add_argument(
        "--mode",
        choices=[
            "webcam",
            "image",
            "video"
        ],
        default="webcam"
    )

    parser.add_argument(
        "--source",
        type=str,
        default=None
    )

    parser.add_argument(
        "--camera",
        type=int,
        default=DEFAULT_CAMERA_INDEX
    )

    parser.add_argument(
        "--conf",
        type=float,
        default=CONFIDENCE_THRESHOLD
    )

    args = parser.parse_args()

    if not 0.0 < args.conf <= 1.0:

        print(
            "Confidence must be between "
            "0 and 1."
        )

        return

    if args.mode == "webcam":

        detect_webcam(
            args.camera,
            args.conf
        )

    elif args.mode == "image":

        if args.source is None:

            print(
                "Please provide --source "
                "for image detection."
            )

            return

        detect_image(
            args.source,
            args.conf
        )

    elif args.mode == "video":

        if args.source is None:

            print(
                "Please provide --source "
                "for video detection."
            )

            return

        detect_video(
            args.source,
            args.conf
        )


if __name__ == "__main__":
    main()