"""
modules/tracker.py
─────────────────────────────────────────────────────
Centroid (Merkez Nokta) Tabanlı Çoklu Kişi Takip Sistemi.

PROBLEM: NEDEN TRACKER GEREKİR?
─────────────────────────────────
Tespit (detection) her frame'de çalışır ve her seferinde
yeni bounding box'lar üretir. Ancak bu kutular birbirine
bağlı değildir. Yani:

  Frame 1: [(100,80,60,150)] → 1 kişi var
  Frame 2: [(102,82,60,150)] → 1 kişi var (aynı kişi mi? farklı mı?)

Takipçi olmadan:
  • 30 saniye boyunca 900 frame → 900 farklı "kişi" sayılır
  • Kişi sayısı anlamsızlaşır
  • "Kişi X kapıdan girdi" gibi mantık kurulamaz

Takipçi ile:
  • Aynı kişiye sürekli aynı ID verilir: #1, #2, #3
  • Sahneye giriş/çıkış zamanı ölçülebilir
  • Her kişi ayrı takip edilir

ALGORİTMA — CENTROID MATCHING:
─────────────────────────────────
1. Her tespite "centroid" (merkez nokta) hesapla
2. Önceki frame'deki centroid'lerle Öklid mesafesini hesapla
3. En yakın çiftleri eşleştir (greedy matching)
4. Mesafe eşikten büyükse → yeni kişi olarak kayıt et
5. Uzun süre eşleşemeyen ID'leri sil

NEDEN DeepSORT/BYTE DEĞİL?
─────────────────────────────
DeepSORT gibi gelişmiş takipçiler Re-ID (yeniden tanıma)
için derin özellik vektörleri kullanır. Güçlüdür ama:
  • Ekstra model dosyası gerektirir
  • GPU olmadan yavaş çalışır
  • Implementasyonu karmaşık

Centroid tracker:
  • Saf Python/NumPy — bağımlılık yok
  • Sabit kamera + orta hız sahnelerde yeterince güvenilir
  • Anlaşılması ve anlatılması kolay

VERI YAPİSİ:
─────────────────────────────────
objects      : {id → centroid}    — aktif kişiler
disappeared  : {id → kayıp sayısı}— kayboluş takibi
trajectories : {id → [centroid listesi]} — hareket geçmişi
─────────────────────────────────────────────────────
"""

import numpy as np
import cv2
from collections import OrderedDict
from config import TRACK_MAX_DISAPPEARED, TRACK_MAX_DISTANCE
from modules.detector import Detection


class CentroidTracker:
    """
    Merkez nokta tabanlı çoklu kişi takipçisi.

    Kullanım:
        tracker = CentroidTracker()

        # Her frame'de:
        detections = tracker.update(detections)
        # Artık her det.track_id dolu

        # Hareket izlerini çiz:
        frame = tracker.draw_trajectories(frame)
    """

    def __init__(self):
        self.next_id     = 1          # İlk atanacak ID (1'den başlar)

        # OrderedDict: ekleme sırasını korur (tekrar üretilebilir davranış)
        self.objects     = OrderedDict()    # {id: centroid(x,y)}
        self.disappeared = OrderedDict()    # {id: kayıp_frame_sayısı}
        self.trajectories = OrderedDict()   # {id: [(x,y), (x,y), ...]}

        # Eşik değerleri (config'den)
        self.max_disappeared = TRACK_MAX_DISAPPEARED
        self.max_distance    = TRACK_MAX_DISTANCE

        # Her ID için farklı renk (max 12 kişi için)
        self._colors = [
            (50, 220, 50),    # yeşil
            (30, 160, 255),   # mavi
            (220, 80, 220),   # mor
            (255, 180, 30),   # turuncu
            (50, 220, 200),   # turkuaz
            (220, 220, 50),   # sarı
            (220, 50, 100),   # pembe
            (150, 100, 255),  # lavanta
            (50, 180, 180),   # camgöbeği
            (200, 200, 120),  # açık sarı
            (100, 180, 100),  # açık yeşil
            (255, 120, 80),   # somon
        ]

    # ──────────────────────────────────────────────────────────
    # ANA GÜNCELLEME METODU
    # ──────────────────────────────────────────────────────────

    def update(self, detections: list) -> list:
        """
        Yeni frame'deki tespitlerle tracker'ı güncelle.
        Her tespite track_id ata ve güncellemiş listeyi döndür.

        Args:
            detections: PersonDetector.detect() çıktısı

        Returns:
            track_id atanmış Detection listesi
        """

        # ── DURUM 1: Hiç tespit yok ───────────────────────────
        if not detections:
            # Tüm aktif nesnelerin kayıp sayacını artır
            for obj_id in list(self.disappeared.keys()):
                self.disappeared[obj_id] += 1

                # Çok uzun süredir kayıpsa → sil
                if self.disappeared[obj_id] > self.max_disappeared:
                    self._deregister(obj_id)

            return []   # Boş liste döndür

        # ── Yeni centroid'leri topla ──────────────────────────
        # shape: (N, 2) — N tespit, her biri (cx, cy)
        input_centroids = np.array([d.centroid for d in detections])

        # ── DURUM 2: Hiç kayıtlı nesne yok → hepsini kaydet ──
        if not self.objects:
            for centroid in input_centroids:
                self._register(centroid)

            # ID'leri tespitlere ata
            for i, det in enumerate(detections):
                det.track_id = list(self.objects.keys())[i]

            return detections

        # ── DURUM 3: Eşleştirme yapılacak ────────────────────
        obj_ids        = list(self.objects.keys())
        obj_centroids  = np.array(list(self.objects.values()))

        # Mesafe matrisi hesapla
        # D[i][j] = objects[i] ile input_centroids[j] arası mesafe
        D = self._euclidean_distance_matrix(obj_centroids, input_centroids)

        # Greedy eşleştirme:
        # Her mevcut nesneyi en yakın yeni tespitle eşleştir
        # Aynı anda bir satır ve sütun sadece bir kez kullanılabilir
        rows = D.min(axis=1).argsort()          # En yakın nesne sırası
        cols = D.argmin(axis=1)[rows]           # Her nesnenin en yakın tespiti

        used_rows = set()
        used_cols = set()
        matched   = {}   # {col_index: obj_id}

        for row, col in zip(rows, cols):
            # Zaten kullanıldıysa atla
            if row in used_rows or col in used_cols:
                continue

            # Mesafe çok büyükse bu eşleştirmeyi yapma
            if D[row, col] > self.max_distance:
                continue

            # Eşleştir
            obj_id = obj_ids[row]
            matched[col] = obj_id

            # Centroid'i güncelle
            self.objects[obj_id]     = input_centroids[col]
            self.disappeared[obj_id] = 0   # Kayıp sayacını sıfırla

            # Hareket izine ekle (son 60 noktayı sakla)
            if obj_id not in self.trajectories:
                self.trajectories[obj_id] = []
            self.trajectories[obj_id].append(tuple(input_centroids[col]))
            if len(self.trajectories[obj_id]) > 60:
                self.trajectories[obj_id].pop(0)

            used_rows.add(row)
            used_cols.add(col)

        # Eşleşmeyen mevcut nesneler → kayıp sayacını artır
        unmatched_rows = set(range(len(obj_ids))) - used_rows
        for row in unmatched_rows:
            obj_id = obj_ids[row]
            self.disappeared[obj_id] += 1
            if self.disappeared[obj_id] > self.max_disappeared:
                self._deregister(obj_id)

        # Eşleşmeyen yeni tespitler → yeni nesne olarak kayıt et
        unmatched_cols = set(range(len(detections))) - used_cols
        for col in unmatched_cols:
            self._register(input_centroids[col])
            matched[col] = self.next_id - 1   # Son atanan ID

        # Track ID'lerini Detection nesnelerine yaz
        for i, det in enumerate(detections):
            det.track_id = matched.get(i, None)

        return detections

    def draw_trajectories(self, frame: np.ndarray) -> np.ndarray:
        """
        Her kişinin geçmiş konumlarını çizgi olarak çiz.
        Çizgi ilerledikçe opaklık artar (en son nokta en belirgin).

        Args:
            frame: Üzerine çizilecek BGR frame

        Returns:
            Hareket izleri eklenmiş frame kopyası
        """
        out = frame.copy()

        for obj_id, traj in self.trajectories.items():
            if len(traj) < 2:
                continue   # En az 2 nokta olmalı

            # Bu ID için renk seç (döngüsel)
            color = self._colors[obj_id % len(self._colors)]

            # Noktalar arası çizgi çiz
            for i in range(1, len(traj)):
                pt1 = traj[i - 1]
                pt2 = traj[i]

                # Çizgi kalınlığı: daha eski nokta = daha ince
                thickness = max(1, int(i / len(traj) * 3))

                cv2.line(out, pt1, pt2, color, thickness, cv2.LINE_AA)

            # En son noktaya küçük daire
            if traj:
                cv2.circle(out, traj[-1], 3, color, -1)

        return out

    def get_count(self) -> int:
        """Şu anda takip edilen kişi sayısı."""
        return len(self.objects)

    def get_color(self, track_id: int) -> tuple:
        """Belirli bir ID için atanan rengi döndür."""
        return self._colors[track_id % len(self._colors)]

    def reset(self):
        """Tüm takip verilerini sıfırla (kamera yeniden başlatılınca)."""
        self.objects.clear()
        self.disappeared.clear()
        self.trajectories.clear()
        self.next_id = 1
        print("[Tracker] Sıfırlandı.")

    # ──────────────────────────────────────────────────────────
    # İÇ YARDIMCILAR
    # ──────────────────────────────────────────────────────────

    def _register(self, centroid: np.ndarray):
        """
        Yeni nesneyi kaydet ve ID ata.

        next_id her kayıtta artırılır — hiç tekrar etmez.
        Bu sayede eski ve yeni kişiler karışmaz.
        """
        self.objects[self.next_id]     = centroid
        self.disappeared[self.next_id] = 0
        print(f"[Tracker] Yeni kişi kaydedildi → ID #{self.next_id}")
        self.next_id += 1

    def _deregister(self, obj_id: int):
        """
        Nesneyi takipten çıkar.

        Trajectory saklanmaya devam eder (tarihsel analiz için).
        Sadece aktif takip sonlandırılır.
        """
        del self.objects[obj_id]
        del self.disappeared[obj_id]
        print(f"[Tracker] ID #{obj_id} takipten çıkarıldı "
              f"({self.max_disappeared} frame görünmedi).")

    @staticmethod
    def _euclidean_distance_matrix(a: np.ndarray, b: np.ndarray) -> np.ndarray:
        """
        İki centroid seti arasında Öklid mesafe matrisi hesapla.

        Formül: sqrt((x2-x1)² + (y2-y1)²)

        Args:
            a: (M, 2) — mevcut nesnelerin centroid'leri
            b: (N, 2) — yeni tespitlerin centroid'leri

        Returns:
            (M, N) mesafe matrisi

        Örnek:
            a = [[100, 200], [300, 400]]   # 2 mevcut nesne
            b = [[105, 205], [295, 395]]   # 2 yeni tespit
            D = [[7.07, 148.2], [141.4, 7.07]]
            → a[0]–b[0] ve a[1]–b[1] eşleşmeli
        """
        # Broadcasting ile tüm çiftleri aynı anda hesapla
        # a[:, np.newaxis, :] → (M, 1, 2)
        # b[np.newaxis, :, :] → (1, N, 2)
        # Fark → (M, N, 2), kareler toplamı → (M, N)
        diff = a[:, np.newaxis, :] - b[np.newaxis, :, :]
        return np.sqrt((diff ** 2).sum(axis=2))
