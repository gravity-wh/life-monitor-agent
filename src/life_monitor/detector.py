import cv2
from typing import Optional, Tuple


class Detector:
    """Placeholder detector using webcam + keyboard for state simulation.
    Keys: r=reading, c=coding, g=guitar, q/ESC=quit.
    Replace key handling with real model inference later.
    """

    def __init__(self, camera_index: int = 0) -> None:
        self.cap = cv2.VideoCapture(camera_index)
        if not self.cap.isOpened():
            print("Warning: Could not open camera. Running without video feed.")
            self.cap = None
        self.current_state: Optional[str] = None

    def get_frame(self):
        if self.cap is None:
            return None
        ok, frame = self.cap.read()
        return frame if ok else None

    def get_state(self, frame) -> Tuple[Optional[str], int]:
        if frame is not None:
            cv2.putText(frame, "r=reading, c=coding, g=guitar, q=quit", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.imshow("Life Monitor", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('r'):
            self.current_state = 'reading'
        elif key == ord('c'):
            self.current_state = 'coding'
        elif key == ord('g'):
            self.current_state = 'guitar'
        return self.current_state, key

    @staticmethod
    def should_quit(key: int) -> bool:
        return key in (27, ord('q'))  # ESC or q

    def release(self) -> None:
        if self.cap is not None:
            self.cap.release()
        try:
            cv2.destroyAllWindows()
        except Exception:
            pass
