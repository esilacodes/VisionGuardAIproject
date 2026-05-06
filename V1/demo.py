

"""
demo.py
─────────────────────────────────────────────────────
VisionGuard AI — Hafta 1 Demo

ÇALIŞTIRILMASI:
    python demo.py

KLAVYE KONTROLLERI:
    Q / ESC  → çık
    N        → gece görüşü aç/kapat
    T        → hareket izlerini aç/kapat
    +        → güven eşiğini artır
    -        → güven eşiğini azalt
    R        → tracker sıfırla
    S        → ekran görüntüsü al
─────────────────────────────────────────────────────
"""

import cv2
import sys
import time
import os
from datetime import datetime

import numpy as np

from config import WINDOW_NAME, WINDOW_WIDTH, WINDOW_HEIGHT, YOLO_CONFIDENCE
from modules.camera   import CameraModule
from modules.detector import PersonDetector
from modules.tracker  import CentroidTracker


# ══════════════════════════════════════════════════════════════
# HUD ÇİZİMİ
# ══════════════════════════════════════════════════════════════

def draw_hud(
    frame:            np.ndarray,
    fps:              float,
    person_count:     int,
    max_simultaneous: int,
    confidence:       float,
    night_mode:       bool,
    show_traj:        bool,
    start_time:       float,
) -> None:
    """
    Frame üzerine bilgi katmanı (HUD) çizer.

    Gösterilen bilgiler:
      Üst bant : FPS, çözünürlük, çalışma süresi, mod etiketleri
      Alt bant : Anlık kişi sayısı, en yüksek eşzamanlı kişi,
                 güven eşiği, klavye kısayolları
    """
    h: int
    w: int
    h, w = frame.shape[:2]

    # ── Üst yarı-saydam bant ──────────────────────────────────
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (w, 42), (15, 15, 30), -1)
    cv2.addWeighted(overlay, 0.72, frame, 0.28, 0, frame)

    # FPS
    cv2.putText(
        frame, f"FPS: {fps:.1f}",
        (10, 18),
        cv2.FONT_HERSHEY_SIMPLEX, 0.52,
        (180, 220, 180), 1, cv2.LINE_AA
    )

    # Çözünürlük + uptime
    elapsed = int(time.time() - start_time)
    m, s    = divmod(elapsed, 60)
    cv2.putText(
        frame, f"{w}x{h}  |  {m:02d}:{s:02d}",
        (10, 35),
        cv2.FONT_HERSHEY_SIMPLEX, 0.42,
        (120, 120, 120), 1, cv2.LINE_AA
    )

    # Sağ üst: aktif mod etiketleri
    x_cursor: int = w - 10
    if night_mode:
        label = "GECE GORUSU"
        color = (80, 200, 255)
        (tw, _), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.45, 1)
        x_cursor -= tw + 14
        cv2.putText(frame, label, (x_cursor, 18),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 1, cv2.LINE_AA)

    if show_traj:
        label = "IZLER ACIK"
        color = (100, 255, 160)
        (tw, _), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.45, 1)
        x_cursor -= tw + 14
        cv2.putText(frame, label, (x_cursor, 18),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 1, cv2.LINE_AA)

    # ── Alt yarı-saydam bant ──────────────────────────────────
    overlay2 = frame.copy()
    cv2.rectangle(overlay2, (0, h - 38), (w, h), (15, 15, 30), -1)
    cv2.addWeighted(overlay2, 0.72, frame, 0.28, 0, frame)

    # Anlık kişi sayısı — kimse yoksa yeşil, varsa mavi
    person_color = (50, 220, 50) if person_count == 0 else (30, 200, 255)
    cv2.putText(
        frame, f"KISI: {person_count}",
        (12, h - 11),
        cv2.FONT_HERSHEY_SIMPLEX, 0.65,
        person_color, 2, cv2.LINE_AA
    )

    # En fazla eşzamanlı kişi sayısı
    # (Bu oturumda en kalabalık an)
    cv2.putText(
        frame, f"Maks: {max_simultaneous}",
        (160, h - 11),
        cv2.FONT_HERSHEY_SIMPLEX, 0.46,
        (150, 150, 150), 1, cv2.LINE_AA
    )

    # Güven eşiği
    cv2.putText(
        frame, f"Guven: {confidence:.0%}",
        (280, h - 11),
        cv2.FONT_HERSHEY_SIMPLEX, 0.46,
        (150, 150, 150), 1, cv2.LINE_AA
    )

    # Klavye kısayolları (sağ alt)
    shortcut = "Q:Cik  N:Gece  T:Iz  +/-:Guven  R:Sifirla  S:Ekran"
    (sw, _), _ = cv2.getTextSize(shortcut, cv2.FONT_HERSHEY_SIMPLEX, 0.34, 1)
    cv2.putText(
        frame, shortcut,
        (w - sw - 6, h - 11),
        cv2.FONT_HERSHEY_SIMPLEX, 0.34,
        (70, 70, 70), 1, cv2.LINE_AA
    )


# ══════════════════════════════════════════════════════════════
# ANA DEMO DÖNGÜSÜ
# ══════════════════════════════════════════════════════════════

def run_demo() -> None:
    print("=" * 55)
    print("  VisionGuard AI — Demo Başlatılıyor")
    print("=" * 55)

    # Modülleri oluştur
    camera:   CameraModule    = CameraModule()
    detector: PersonDetector  = PersonDetector()
    tracker:  CentroidTracker = CentroidTracker()

    # Kamerayı başlat
    try:
        camera.start()
    except RuntimeError as e:
        print(f"\n[HATA] {e}")
        sys.exit(1)

    # İlk frame gelene kadar bekle (max 5 saniye)
    print("[Demo] İlk frame bekleniyor...", end="", flush=True)
    deadline = time.time() + 5.0
    while camera.get_frame() is None:
        time.sleep(0.05)
        if time.time() > deadline:
            print("\n[HATA] Kameradan frame alınamadı.")
            camera.stop()
            sys.exit(1)
    print(" ✓")

    # OpenCV penceresi
    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(WINDOW_NAME, WINDOW_WIDTH, WINDOW_HEIGHT)

    # Durum değişkenleri
    show_trajectories: bool  = False
    confidence:        float = float(YOLO_CONFIDENCE)
    start_time:        float = time.time()

    # Kişi sayısı takibi
    # max_simultaneous: bu oturumda aynı anda en fazla kaç kişi görüldü
    max_simultaneous:  int   = 0

    os.makedirs("data/screenshots", exist_ok=True)

    print("\n[Demo] Çalışıyor.")
    print("  Q/ESC → çık  |  N → gece  |  T → izler")
    print("  +/-   → güven  |  R → sıfırla  |  S → ekran görüntüsü\n")

    # ── Ana döngü ─────────────────────────────────────────────
    while True:

        # 1. Kameradan en güncel frame'i al
        frame: np.ndarray | None = camera.get_frame()
        if frame is None:
            continue

        # 2. YOLOv8 ile insan tespiti
        detections = detector.detect(frame)

        # 3. Centroid Tracker ile ID atama
        detections = tracker.update(detections)

        # 4. Anlık kişi sayısını al
        current_count = tracker.get_count()

        # Eşzamanlı maksimum kişiyi güncelle
        # NOT: next_id değil, get_count() kullanıyoruz
        # get_count() → şu an ekranda kaç kişi var
        # next_id    → toplam kaç ID atandı (her kaybolmada artar, yanıltıcı)
        if current_count > max_simultaneous:
            max_simultaneous = current_count

        # 5. Görselleştirme
        if show_trajectories:
            frame = tracker.draw_trajectories(frame)

        frame = detector.draw(frame, detections)

        draw_hud(
            frame            = frame,
            fps              = camera.get_fps(),
            person_count     = current_count,
            max_simultaneous = max_simultaneous,
            confidence       = confidence,
            night_mode       = detector.night_mode,
            show_traj        = show_trajectories,
            start_time       = start_time,
        )

        # 6. Göster
        cv2.imshow(WINDOW_NAME, frame)

        # 7. Klavye kontrolü
        key: int = cv2.waitKey(1) & 0xFF

        if key in (ord("q"), ord("Q"), 27):
            print("\n[Demo] Çıkış yapılıyor...")
            break

        elif key in (ord("n"), ord("N")):
            detector.toggle_night_mode()  # type: ignore[union-attr]

        elif key in (ord("t"), ord("T")):
            show_trajectories = not show_trajectories
            durum = "ACIK" if show_trajectories else "KAPALI"
            print(f"[Demo] Hareket izleri → {durum}")

        elif key in (ord("+"), ord("=")):
            confidence = min(0.95, confidence + 0.05)
            detector.set_confidence(confidence)  # type: ignore[union-attr]

        elif key == ord("-"):
            confidence = max(0.10, confidence - 0.05)
            detector.set_confidence(confidence)  # type: ignore[union-attr]

        elif key in (ord("r"), ord("R")):
            tracker.reset()
            max_simultaneous = 0
            print("[Demo] Tracker sıfırlandı.")

        elif key in (ord("s"), ord("S")):
            ts   = datetime.now().strftime("%Y%m%d_%H%M%S")
            path = f"data/screenshots/demo_{ts}.jpg"
            cv2.imwrite(path, frame)  # type: ignore[arg-type]
            print(f"[Demo] Kaydedildi → {path}")

        # Pencere X ile kapatıldıysa çık
        try:
            if cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
                break
        except cv2.error:
            break

    # ── Temiz kapanış ─────────────────────────────────────────
    camera.stop()
    cv2.destroyAllWindows()

    elapsed = int(time.time() - start_time)
    m, s    = divmod(elapsed, 60)
    print(f"\n[Demo] Tamamlandı.")
    print(f"  Süre         : {m:02d}:{s:02d}")
    print(f"  Toplam frame : {camera.frame_count}")
    print(f"  Maks kişi    : {max_simultaneous}")


# ══════════════════════════════════════════════════════════════
# GİRİŞ NOKTASI
# ══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    run_demo()