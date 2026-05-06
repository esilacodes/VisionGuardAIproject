

"""
modules/camera.py
─────────────────────────────────────────────────────
Camera access and frame management module.

WHY A SEPARATE THREAD?
OpenCV's cap.read() function is a blocking call.
It waits until the camera provides a frame.

If frame reading is done inside the main GUI loop:
    • UI freezes
    • Detection becomes delayed
    • FPS drops

Solution:
Run camera capture inside a separate daemon thread.
The main application always reads the latest available frame
without waiting.

This follows the Producer-Consumer pattern.

THREAD SAFETY:
The camera thread writes to _frame while the main thread reads it.
Simultaneous access may corrupt data.

threading.Lock() guarantees safe access.
─────────────────────────────────────────────────────
"""

import cv2
import threading
import time

from config import (
    CAMERA_INDEX,
    CAMERA_WIDTH,
    CAMERA_HEIGHT,
    CAMERA_FPS
)


class CameraModule:
    """
    Camera manager class using a separate capture thread.

    Usage:
        cam = CameraModule()
        cam.start()

        frame = cam.get_frame()
        fps = cam.get_fps()

        cam.stop()
    """

    def __init__(self):

        # OpenCV camera object
        self.cap = None

        # Thread state
        self.running = False
        self._thread = None

        # Shared frame data
        self._frame = None

        # Thread safety lock
        self._lock = threading.Lock()

        # Statistics
        self.frame_count = 0
        self._fps = 0.0
        self._fps_counter = 0
        self._fps_timer = 0.0

    # ─────────────────────────────────────────────
    # START CAMERA
    # ─────────────────────────────────────────────

    def start(self) -> bool:
        """
        Open the camera and start capture thread.

        Returns:
            bool: True if successful

        Raises:
            RuntimeError: If camera cannot be opened
        """

        # Create VideoCapture object
        self.cap = cv2.VideoCapture(CAMERA_INDEX)

        # Check if camera opened successfully
        if not self.cap.isOpened():
            raise RuntimeError(
                f"Failed to open camera (index={CAMERA_INDEX})\n"
                "Check:\n"
                "1. Is the camera connected?\n"
                "2. Is another application using it?\n"
                "3. Are drivers installed?"
            )

        # Configure camera properties
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
        self.cap.set(cv2.CAP_PROP_FPS, CAMERA_FPS)

        # Reduce buffer size to minimize latency
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        # Read actual resolution
        actual_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        actual_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        print(
            f"[Camera] Started -> "
            f"{actual_width}x{actual_height} @ {CAMERA_FPS} FPS"
        )

        # Reset statistics
        self.running = True
        self.frame_count = 0
        self._fps_counter = 0
        self._fps_timer = time.time()

        # Create daemon thread
        self._thread = threading.Thread(
            target=self._capture_loop,
            daemon=True,
            name="CameraThread"
        )

        self._thread.start()

        print(f"[Camera] Thread started -> {self._thread.name}")

        return True

    # ─────────────────────────────────────────────
    # STOP CAMERA
    # ─────────────────────────────────────────────

    def stop(self) -> None:
        """
        Stop camera and release resources.
        """

        self.running = False

        # Wait for thread to finish
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=2.0)

        # Release camera
        if self.cap is not None:
            self.cap.release()
            self.cap = None

        # Clear frame
        self._frame = None

        print("[Camera] Stopped and resources released.")

    # ─────────────────────────────────────────────
    # GET FRAME
    # ─────────────────────────────────────────────

    def get_frame(self):
        """
        Return latest captured frame safely.

        Returns:
            numpy.ndarray | None
        """

        with self._lock:

            if self._frame is None:
                return None

            # Return copy to avoid shared memory issues
            return self._frame.copy()

    # ─────────────────────────────────────────────
    # GET FPS
    # ─────────────────────────────────────────────

    def get_fps(self) -> float:
        """
        Return current FPS value.
        """

        return round(self._fps, 1)

    # ─────────────────────────────────────────────
    # GET RESOLUTION
    # ─────────────────────────────────────────────

    def get_resolution(self) -> tuple[int, int]:
        """
        Return current camera resolution.
        """

        if self.cap is not None:
            return (
                int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            )

        return (0, 0)

    # ─────────────────────────────────────────────
    # THREAD STATUS
    # ─────────────────────────────────────────────

    def is_alive(self) -> bool:
        """
        Check whether camera thread is alive.
        """

        return (
            self.running and
            self._thread is not None and
            self._thread.is_alive()
        )

    # ─────────────────────────────────────────────
    # CAPTURE LOOP
    # ─────────────────────────────────────────────

    def _capture_loop(self) -> None:
        """
        Internal camera capture loop.

        Runs continuously until:
            • stop() is called
            • camera disconnects
        """

        # Safety check
        if self.cap is None:
            return

        while self.running:

            # Read frame from camera
            ret, frame = self.cap.read()

            # Successful frame capture
            if ret:

                # Thread-safe frame update
                with self._lock:
                    self._frame = frame.copy()

                # Statistics
                self.frame_count += 1
                self._fps_counter += 1

                # Calculate FPS every second
                now = time.time()
                elapsed = now - self._fps_timer

                if elapsed >= 1.0:

                    self._fps = self._fps_counter / elapsed

                    self._fps_counter = 0
                    self._fps_timer = now

            else:
                print(
                    "[Camera] Failed to read frame. "
                    "Camera connection may be lost."
                )

                self.running = False
                break



