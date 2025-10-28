try:
    import cv2  # optional; used when implemented
except Exception:
    cv2 = None

class ImageDetector:
    def __init__(self, camera_index: int = 0) -> None:
        self.camera_index = camera_index

    def run(self) -> None:
        # TODO: Implement image detection and publish events
        pass
