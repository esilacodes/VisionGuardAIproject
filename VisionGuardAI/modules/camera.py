"""
modules/camera.py
OpenCV camera access and frame management.
The camera runs in a separate thread — the UI never freezes.
"""
import cv2
import threading

from matplotlib.pyplot import cla
from sympy import false, true
from config import CAMERA_INDEX

class CameraModule:
    def __init__(self) :
        """Initializes camera variables and thread-safe frame storage."""
        self.cap=None
        self.running=False
        self._frame=None
        self._lock=threading.Lock()
        self._thread=None

    def start(self) -> bool:
        """Starts the camera stream in a separate background thread."""
        self.cap=cv2.VideoCapture(CAMERA_INDEX)
        if not self.cap.isOpened():
            raise RuntimeError(
               f"Camera {CAMERA_INDEX} could not be opened. "
                "Check if it is connected or used by another application."
            )
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
        self.running=True
        self._thread=threading.Thread(
            target=self._capture_loop,
            daemon=True,
            name="CameraTHread"
        )
        self._thread.start()
        return True
    
    def stop(self) ->None:
        """Stops the camera stream and releases all resources."""
        self.running=False
        if self._thread:
            self._thread.join(timeout=2)
        if self.cap:
            self.cap.release()
        self.cap=None
        self._frame=None

    def get_frame(self):
        """Returns the latest captured frame safely."""
        with self._lock:
            if self._frame is None:
                return None
        return self._frame.copy()

    def is_alive(self)-> bool:
        """Checks whether the camera thread is still running."""
        return self.running and self._thread is not None and self._thread.is_alive()

    def _capture_loop(self)-> None:
        """Continuously captures frames until the camera is stopped."""
        while self.running:
            ret,frame=self.cap.read()
            if ret:
                with self._lock:
                    self._frame=frame
            else:
                # Camera disconnected or failed
                self.running=False
                break        







