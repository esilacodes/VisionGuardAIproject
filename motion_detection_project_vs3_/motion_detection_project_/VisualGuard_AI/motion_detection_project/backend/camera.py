"""
camera.py — Kamera ve hareket algılama yönetimi

─────────────────────────────────────────────────────────
KENDI ALGOIRTMANIZI BAĞLAMAK İÇİN:
─────────────────────────────────────────────────────────
1. Kendi .py dosyanızı backend/ klasörüne koyun.
   Örnek: backend/my_detector.py

2. O dosyada şu iki fonksiyonu tanımlayın:

       def open_camera(index: int):
           # cv2.VideoCapture veya kendi nesnenizi döndürün
           # Açılamazsa None döndürün
           ...

       def detect(prev_frame, curr_frame, sensitivity: int) -> bool:
           # prev_frame, curr_frame: PIL Image
           # sensitivity: 0-100 arası int
           # Hareket varsa True döndürün
           ...

3. Aşağıdaki CUSTOM_DETECTOR satırını düzenleyin:

       CUSTOM_DETECTOR = "my_detector"   # backend/my_detector.py

   Kullanmak istemiyorsanız None bırakın:
       CUSTOM_DETECTOR = None
─────────────────────────────────────────────────────────
"""

import io
import time
import random
import threading
import importlib
from datetime import datetime
from PIL import Image, ImageDraw

try:
    import cv2
    import numpy as np
    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False

# ─── BURAYA KENDİ MODÜL ADINIZI YAZIN ────────────────────
CUSTOM_DETECTOR = None   # Örnek: "my_detector"
# ─────────────────────────────────────────────────────────


def _load_custom_detector():
    """CUSTOM_DETECTOR tanımlıysa yükle, yoksa None döndür."""
    if not CUSTOM_DETECTOR:
        return None
    try:
        mod = importlib.import_module(f"backend.{CUSTOM_DETECTOR}")
        required = ("open_camera", "detect")
        for fn in required:
            if not hasattr(mod, fn):
                print(f"⚠️  backend/{CUSTOM_DETECTOR}.py içinde '{fn}' fonksiyonu bulunamadı.")
                return None
        print(f"✅ Özel dedektör yüklendi: backend/{CUSTOM_DETECTOR}.py")
        return mod
    except ModuleNotFoundError:
        print(f"⚠️  backend/{CUSTOM_DETECTOR}.py bulunamadı — varsayılan algılama kullanılıyor.")
        return None


class CameraManager:
    """
    Kamera yönetimi — gerçek webcam veya simülasyon modu.
    Dashboard ve Live sekmeleri bu sınıfı paylaşır.
    """

    def __init__(self):
        self._cap = None
        self.is_detecting = False
        self._thread = None
        self._on_frame = None
        self._on_detection = None
        self._detector = _load_custom_detector()

    # ──────────────────────────────────────────
    # Public API
    # ──────────────────────────────────────────

    def start(self, sensitivity: int, on_frame, on_detection):
        """
        Kamerayı başlat.

        Args:
            sensitivity:  0-100 arası hareket hassasiyeti
            on_frame:     Her frame'de çağrılır → on_frame(pil_image)
            on_detection: Hareket tespit edilince → on_detection(image_bytes)
        """
        if self.is_detecting:
            return

        self._on_frame = on_frame
        self._on_detection = on_detection
        self.is_detecting = True

        # Kamerayı aç (özel dedektör veya varsayılan)
        if self._detector:
            self._cap = self._detector.open_camera(0)
        elif OPENCV_AVAILABLE:
            cap = cv2.VideoCapture(0)
            self._cap = cap if cap.isOpened() else None
        else:
            self._cap = None

        self._thread = threading.Thread(
            target=self._detection_loop,
            args=(sensitivity,),
            daemon=True
        )
        self._thread.start()

    def stop(self):
        """Kamerayı durdur ve kaynakları serbest bırak."""
        self.is_detecting = False
        if self._cap:
            try:
                self._cap.release()
            except Exception:
                pass
            self._cap = None

    @property
    def has_real_camera(self):
        return self._cap is not None

    def read_frame(self):
        """Kameradan PIL Image döndür. Webcam yoksa None."""
        if self._cap and self._cap.isOpened():
            ret, frame = self._cap.read()
            if ret:
                return Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        return None

    # ──────────────────────────────────────────
    # Hareket algılama döngüsü (thread)
    # ──────────────────────────────────────────

    def _detection_loop(self, sensitivity: int):
        prev_pil = None
        last_detection_time = 0
        detection_count = 0

        while self.is_detecting:
            time.sleep(0.1)

            if not self.is_detecting:
                break

            if self._cap and self._cap.isOpened():
                # ── Gerçek kamera ──────────────────────
                curr_pil = self.read_frame()
                if curr_pil is None:
                    continue

                if self._on_frame:
                    self._on_frame(curr_pil)

                # Hareket algılama (özel veya varsayılan)
                if self._detector:
                    motion = self._detector.detect(prev_pil, curr_pil, sensitivity)
                else:
                    motion = self._default_detect(prev_pil, curr_pil, sensitivity)

                prev_pil = curr_pil

                if motion and (time.time() - last_detection_time) >= 3:
                    last_detection_time = time.time()
                    detection_count += 1
                    if self._on_detection:
                        self._on_detection(self._pil_to_bytes(curr_pil))

            else:
                # ── Simülasyon modu ────────────────────
                time.sleep(random.uniform(2, 5) - 0.1)
                if not self.is_detecting:
                    break
                detection_count += 1
                img_bytes = self._create_dummy_image(detection_count)
                if self._on_frame:
                    self._on_frame(Image.open(io.BytesIO(img_bytes)))
                if self._on_detection:
                    self._on_detection(img_bytes)

    # ──────────────────────────────────────────
    # Varsayılan hareket algılama
    # ──────────────────────────────────────────

    @staticmethod
    def _default_detect(prev, curr, sensitivity: int) -> bool:
        if prev is None or not OPENCV_AVAILABLE:
            return False
        prev_gray = cv2.cvtColor(np.array(prev), cv2.COLOR_RGB2GRAY)
        curr_gray = cv2.cvtColor(np.array(curr), cv2.COLOR_RGB2GRAY)
        diff = cv2.absdiff(prev_gray, curr_gray)
        _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
        motion_ratio = (thresh.sum() / 255) / (thresh.shape[0] * thresh.shape[1]) * 100
        return motion_ratio > (100 - sensitivity)

    # ──────────────────────────────────────────
    # Yardımcılar
    # ──────────────────────────────────────────

    @staticmethod
    def _pil_to_bytes(img: Image.Image) -> bytes:
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        return buf.getvalue()

    @staticmethod
    def _create_dummy_image(n: int) -> bytes:
        img = Image.new('RGB', (640, 480), color=(45, 62, 80))
        draw = ImageDraw.Draw(img)
        x, y = random.randint(80, 450), random.randint(80, 320)
        clr = random.choice(['#E74C3C', '#2ECC71', '#F1C40F', '#3498DB', '#9B59B6'])
        draw.rectangle([x, y, x + 160, y + 120], outline=clr, width=3)
        draw.text((20, 20), f"Simulation — Detection #{n}", fill='white')
        draw.text((20, 50), datetime.now().strftime('%Y-%m-%d  %H:%M:%S'), fill='#BDC3C7')
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        return buf.getvalue()


# Global instance
camera_manager = CameraManager()
