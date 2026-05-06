"""
modules/detector.py
─────────────────────────────────────────────────────
YOLOv8 tabanlı gerçek zamanlı insan tespiti modülü
ve absDiff fallback sistemi.
─────────────────────────────────────────────────────
"""
# type: ignore
import cv2
import numpy as np
from typing import Optional

from config import (
    YOLO_MODEL,
    YOLO_CONFIDENCE,
    YOLO_PERSON_CLASS,
    MOTION_THRESHOLD,
    NIGHT_MODE_THRESHOLD
)


# ═════════════════════════════════════════════════════
# DETECTION CLASS
# ═════════════════════════════════════════════════════

class Detection:
    """
    Tek bir tespit sonucunu tutan veri sınıfı.

    Attributes:
        bbox       : (x, y, w, h) — sol üst köşe + boyutlar
        confidence : 0.0–1.0 güven skoru
        track_id   : Tracker tarafından atanır, başta None
        centroid   : Bounding box merkez noktası (cx, cy)
    """

    def __init__(
        self,
        bbox:       tuple,
        confidence: float,
        track_id:   Optional[int] = None
    ):
        self.bbox       = bbox
        self.confidence = confidence
        self.track_id   = track_id

        # Centroid (merkez nokta) hesapla
        # Tracker bu noktayı kullanarak kişileri eşleştirir
        x, y, w, h     = bbox
        self.centroid   = (x + w // 2, y + h // 2)

    def __repr__(self) -> str:
        return (
            f"Detection("
            f"id={self.track_id}, "
            f"conf={self.confidence:.2f}, "
            f"bbox={self.bbox})"
        )


# ═════════════════════════════════════════════════════
# PERSON DETECTOR
# ═════════════════════════════════════════════════════

class PersonDetector:
    """
    YOLOv8 ile gerçek zamanlı insan tespiti.

    Kullanım:
        detector = PersonDetector()
        detections = detector.detect(frame)
        frame_out  = detector.draw(frame, detections)
    """

    def __init__(self):
        self.model:      Optional[object] = None
        self.use_yolo:   bool             = False
        self.night_mode: bool             = False

        self._prev_gray:   Optional[np.ndarray] = None
        self._confidence:  float                = YOLO_CONFIDENCE

        # CLAHE — bir kez oluştur, her frame'de yeniden kullan
        # clipLimit=3.0  → kontrast artış sınırı
        # tileGridSize   → adaptif blok boyutu
        self._clahe = cv2.createCLAHE(
            clipLimit=3.0,
            tileGridSize=(8, 8)
        )

        self._load_model()

    # ─────────────────────────────────────────────────
    # MODEL YÜKLEME
    # ─────────────────────────────────────────────────

    def _load_model(self) -> None:
        """
        YOLOv8n modelini yükle.
        İlk çalıştırmada ~6MB model internetten indirilir.
        Hata olursa absDiff fallback'e geçilir, sistem durmaz.
        """
        try:
            from ultralytics import YOLO
            print(f"[Detector] YOLO loading: {YOLO_MODEL}")
            self.model    = YOLO(YOLO_MODEL)
            self.use_yolo = True
            print("[Detector] YOLO ready ✓")

        except ImportError:
            print(
                "[Detector] ultralytics bulunamadı.\n"
                "           pip install ultralytics\n"
                "           Fallback → absDiff modu"
            )
        except Exception as e:
            print(f"[Detector] Model yüklenemedi: {e}\n"
                  "           Fallback → absDiff modu")

    # ─────────────────────────────────────────────────
    # ANA TESPİT API
    # ─────────────────────────────────────────────────

    def detect(self, frame: np.ndarray) -> list:
        """
        Frame üzerinde insan tespiti yap.

        Sıra:
          1. Gece görüşü ön işlemesi (gerekiyorsa CLAHE)
          2. YOLOv8 veya absDiff ile tespit
          3. Detection listesi döndür

        Returns:
            list[Detection] — boş olabilir
        """
        processed = self._preprocess(frame)

        if self.use_yolo:
            return self._detect_yolo(processed)

        return self._detect_absdiff(processed)

    # ─────────────────────────────────────────────────
    # ÇIZIM
    # ─────────────────────────────────────────────────

    def draw(self, frame: np.ndarray, detections: list) -> np.ndarray:
        """
        Tespitleri frame üzerine çiz.

        Çizilen öğeler:
          • Bounding box (renkli dikdörtgen)
          • Etiket arka planı + ID + güven skoru
          • Centroid noktası + ince halka
          • Sol alt: aktif mod bilgisi

        Args:
            frame      : Orijinal BGR frame (değiştirilmez)
            detections : detect() çıktısı

        Returns:
            Çizimler eklenmiş kopya frame
        """
        out = frame.copy()   # Orijinali korumak için kopya al

        for det in detections:
            x, y, w, h = det.bbox

            # Takip edilen kişi → yeşil, henüz ID yok → turuncu
            color = (50, 220, 50) if det.track_id else (30, 180, 255)

            # Etiket: ID + güven skoru
            label = ""
            if det.track_id:
                label += f"#{det.track_id}  "
            label += f"Kisi {det.confidence:.0%}"

            # Bounding box
            cv2.rectangle(out, (x, y), (x + w, y + h), color, 2)

            # Etiket arka planı (okunabilirlik için)
            (txt_w, txt_h), _ = cv2.getTextSize(
                label, cv2.FONT_HERSHEY_SIMPLEX, 0.55, 1
            )
            cv2.rectangle(
                out,
                (x, y - txt_h - 10),
                (x + txt_w + 8, y),
                color,
                -1   # dolu
            )

            # Etiket metni
            cv2.putText(
                out, label,
                (x + 4, y - 5),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55,
                (255, 255, 255), 1, cv2.LINE_AA
            )

            # Centroid: dolu daire + ince halka
            cx, cy = det.centroid
            cv2.circle(out, (cx, cy), 4, color, -1)
            cv2.circle(out, (cx, cy), 8, color, 1)

        # Sol alt köşe: aktif mod
        mode = "YOLOv8n" if self.use_yolo else "absDiff (fallback)"
        if self.night_mode:
            mode += " | GECE GORUSU"

        cv2.putText(
            out, mode,
            (8, frame.shape[0] - 8),
            cv2.FONT_HERSHEY_SIMPLEX, 0.40,
            (130, 130, 130), 1, cv2.LINE_AA
        )

        return out

    # ─────────────────────────────────────────────────
    # AYARLAR
    # ─────────────────────────────────────────────────

    def set_confidence(self, value: float) -> None:
        """
        Güven eşiğini güncelle.
        Demo sırasında +/- tuşlarıyla çağrılır.
        """
        self._confidence = max(0.10, min(0.95, float(value)))
        print(f"[Detector] Güven eşiği → {self._confidence:.0%}")

    def toggle_night_mode(self) -> None:
        """Gece görüşünü aç/kapat."""
        self.night_mode = not self.night_mode
        durum = "AKTİF" if self.night_mode else "KAPALI"
        print(f"[Detector] Gece görüşü → {durum}")

    # ─────────────────────────────────────────────────
    # ÖN İŞLEME — GECE GÖRÜŞÜ (CLAHE)
    # ─────────────────────────────────────────────────

    def _preprocess(self, frame: np.ndarray) -> np.ndarray:
        """
        Gece görüşü ön işlemesi.

        Otomatik: ortalama parlaklık eşiğin altına düşerse devreye girer.
        Manuel  : toggle_night_mode() ile kullanıcı açar/kapatır.

        CLAHE LAB uzayında sadece L (parlaklık) kanalına uygulanır.
        A ve B (renk) kanalları değişmez — renkler korunur.
        """
        gray       = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        brightness = float(np.mean(gray))

        # Ortam çok karanlıksa otomatik gece modu
        if brightness < NIGHT_MODE_THRESHOLD:
            self.night_mode = True

        if not self.night_mode:
            return frame   # Normal modda işlem yok

        # BGR → LAB
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)

        # Kanalları ayır
        l_channel, a_channel, b_channel = cv2.split(lab)

        # Sadece L kanalına CLAHE uygula
        l_enhanced = self._clahe.apply(l_channel)

        # Kanalları birleştir (liste kullan — Pylance uyumlu)
        lab_merged = cv2.merge([l_enhanced, a_channel, b_channel])

        # LAB → BGR
        return cv2.cvtColor(lab_merged, cv2.COLOR_LAB2BGR)

    # ─────────────────────────────────────────────────
    # YOLO TESPİTİ
    # ─────────────────────────────────────────────────

    def _detect_yolo(self, frame: np.ndarray) -> list:
        """
        YOLOv8 ile insan tespiti.

        classes=[0]   → sadece 'person' sınıfı (COCO class 0)
        conf=...      → minimum güven filtresi
        verbose=False → terminal spam'ini kapat

        YOLO xyxy formatında döner, biz xywh'ye çeviririz.
        """
        if self.model is None:
            return []

        results = self.model(
            frame,
            classes=[YOLO_PERSON_CLASS],
            conf=self._confidence,
            verbose=False
        )

        detections = []

        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf            = float(box.conf[0])

                # xyxy → xywh
                detections.append(
                    Detection((x1, y1, x2 - x1, y2 - y1), conf)
                )

        return detections

    # ─────────────────────────────────────────────────
    # ABSDIFF FALLBACK
    # ─────────────────────────────────────────────────

    def _detect_absdiff(self, frame: np.ndarray) -> list:
        """
        Klasik frame farkı yöntemi (YOLO yoksa çalışır).

        Adımlar:
          1. BGR → gri
          2. Gaussian blur (gürültü azalt)
          3. absDiff → iki frame arası fark
          4. Threshold → binary maske
          5. Dilate → boşlukları kapat
          6. Kontur bul → bounding box çıkar
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # İlk frame — karşılaştıracak önceki frame yok
        if self._prev_gray is None:
            self._prev_gray = gray
            return []

        diff      = cv2.absdiff(self._prev_gray, gray)
        _, mask   = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
        kernel    = np.ones((3, 3), np.uint8)
        mask      = cv2.dilate(mask, kernel, iterations=2)

        contours, _ = cv2.findContours(
            mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        self._prev_gray = gray

        detections = []
        for cnt in contours:
            if cv2.contourArea(cnt) > MOTION_THRESHOLD:
                x, y, w, h = cv2.boundingRect(cnt)
                # absDiff güven skoru üretemez — sabit değer
                detections.append(Detection((x, y, w, h), 0.6))

        return detections
