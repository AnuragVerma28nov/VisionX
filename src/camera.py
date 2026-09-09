import cv2


def find_available_cameras(max_cameras=5):

    available_cameras = []

    for index in range(max_cameras):

        camera = cv2.VideoCapture(index)

        if camera.isOpened():
            available_cameras.append(index)

        camera.release()

    return available_cameras


class Camera:

    def __init__(self, camera_index=0):

        self.camera_index = camera_index

        self.cap = cv2.VideoCapture(camera_index)

    def is_opened(self):

        return self.cap.isOpened()

    def read(self):

        return self.cap.read()

    def release(self):

        self.cap.release()