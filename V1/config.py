"""
config.py
─────────────────────────────────────────────────────
VisionGuard AI — Merkezi Yapılandırma Dosyası

Tüm sabit değerler ve ayarlar buradan yönetilir.
Bir ayarı değiştirmek için yalnızca bu dosyaya dokunman yeterli.
─────────────────────────────────────────────────────
"""

# ── Kamera Ayarları ───────────────────────────────────────────
CAMERA_INDEX  = 0        # 0 = varsayılan kamera, 1 = ikinci kamera
CAMERA_WIDTH  = 640      # Yakalama çözünürlüğü (piksel)
CAMERA_HEIGHT = 480
CAMERA_FPS    = 30       # Hedef FPS (kamera destekliyorsa)

# ── YOLOv8 Ayarları ──────────────────────────────────────────
YOLO_MODEL        = "yolov8n.pt"   # n=nano (en hızlı), s/m/l/x = daha doğru ama yavaş
YOLO_CONFIDENCE   = 0.45           # Minimum güven skoru (0.0–1.0)
                                   # Düşük → daha fazla tespit, fazla false alarm
                                   # Yüksek → daha az tespit, daha güvenilir
YOLO_PERSON_CLASS = 0              # COCO veri setinde 0 = "person"

# ── Takip (Tracker) Ayarları ──────────────────────────────────
TRACK_MAX_DISAPPEARED = 20   # Kaç frame görünmeyince ID silinsin
                             # Düşük → ID'ler hızlı silinir (titreme riski)
                             # Yüksek → uzun süre "hayalet" ID kalabilir
TRACK_MAX_DISTANCE    = 120   # Piksel cinsinden maksimum eşleştirme mesafesi
                             # İki frame arasında kişi bu kadar hareket edebilir

# ── absDiff Fallback (YOLO yoksa) ────────────────────────────
MOTION_THRESHOLD = 500       # Minimum kontur alanı (piksel²)
                             # Küçük değer → gürültüye duyarlı
                             # Büyük değer → yavaş/küçük hareketler kaçabilir

# ── Gece Görüşü ──────────────────────────────────────────────
NIGHT_MODE_THRESHOLD = 60    # Ortalama parlaklık bu değerin altına düşünce
                             # gece görüşü otomatik devreye girer (0–255)

# ── Demo Penceresi ───────────────────────────────────────────
WINDOW_NAME   = "VisionGuard AI — Demo"
WINDOW_WIDTH  = 960    # Demo penceresinin genişliği
WINDOW_HEIGHT = 540    # Demo penceresinin yüksekliği
