
import cv2
import threading
import time
from telegram_service import send_message

class Camera:
    def __init__(self):
        self.running = False
        self.sensitivity = 5000
        self.last_frame = None

    def start(self):
        self.running = True
        threading.Thread(target=self._loop, daemon=True).start()

    def stop(self):
        self.running = False

    def _loop(self):
        cap = cv2.VideoCapture(0)

        while self.running:
            ret, frame = cap.read()
            if not ret:
                continue

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            if self.last_frame is None:
                self.last_frame = gray
                continue

            diff = cv2.absdiff(self.last_frame, gray)
            score = diff.sum()

            if score > self.sensitivity:
                send_message("Motion detected!")
                time.sleep(2)

            self.last_frame = gray

        cap.release()
