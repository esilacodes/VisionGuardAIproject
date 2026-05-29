"""
my_detector_TEMPLATE.py — Kendi hareket algılama modülünüz için şablon
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

KULLANIM:
  1. Bu dosyayı kopyalayın → backend/my_detector.py
  2. open_camera() ve detect() fonksiyonlarını doldurun
  3. camera.py dosyasında şu satırı güncelleyin:
         CUSTOM_DETECTOR = "my_detector"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

from PIL import Image


def open_camera(index: int):
    """
    Kamerayı aç ve döndür.

    Args:
        index: Kamera index numarası (genellikle 0 = dahili webcam)

    Returns:
        Kamera nesnesi (.isOpened() ve .read() metodları olmalı)
        Açılamazsa None döndürün.

    Örnek (OpenCV):
        import cv2
        cap = cv2.VideoCapture(index)
        return cap if cap.isOpened() else None
    """
    # ── BURAYA KENDİ KODUNUZU YAZIN ──────────────────────────
    import cv2
    cap = cv2.VideoCapture(index)
    return cap if cap.isOpened() else None
    # ─────────────────────────────────────────────────────────


def detect(prev_frame, curr_frame, sensitivity: int) -> bool:
    """
    İki frame arasında hareket var mı?

    Args:
        prev_frame:  Önceki frame (PIL Image veya None — ilk frame'de None gelir)
        curr_frame:  Mevcut frame (PIL Image)
        sensitivity: Kullanıcının ayarladığı hassasiyet (0-100)
                     Yüksek = daha hassas = küçük hareketleri de yakala

    Returns:
        True  → hareket tespit edildi, kayıt alınsın
        False → hareket yok

    Örnek (basit piksel farkı):
        import cv2, numpy as np
        if prev_frame is None:
            return False
        prev = cv2.cvtColor(np.array(prev_frame), cv2.COLOR_RGB2GRAY)
        curr = cv2.cvtColor(np.array(curr_frame), cv2.COLOR_RGB2GRAY)
        diff = cv2.absdiff(prev, curr)
        _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
        ratio = (thresh.sum() / 255) / (thresh.shape[0] * thresh.shape[1]) * 100
        return ratio > (100 - sensitivity)
    """
    # ── BURAYA KENDİ KODUNUZU YAZIN ──────────────────────────
    if prev_frame is None:
        return False

    import cv2
    import numpy as np

    prev = cv2.cvtColor(np.array(prev_frame), cv2.COLOR_RGB2GRAY)
    curr = cv2.cvtColor(np.array(curr_frame), cv2.COLOR_RGB2GRAY)
    diff = cv2.absdiff(prev, curr)
    _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
    ratio = (thresh.sum() / 255) / (thresh.shape[0] * thresh.shape[1]) * 100
    return ratio > (100 - sensitivity)
    # ─────────────────────────────────────────────────────────
