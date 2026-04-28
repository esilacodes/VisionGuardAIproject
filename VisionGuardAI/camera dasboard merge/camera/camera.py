import cv2
import threading
import numpy as np
from typing import Optional
import sys
import os

# config.py dosyasını bulabilmesi için proje kök dizinini yola ekliyoruz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from config import CAMERA_INDEX
except ImportError:
    print("Uyarı: config.py bulunamadı, varsayılan kamera indeksi 0 kullanılıyor.")
    CAMERA_INDEX = 0

class CameraModule:
    def __init__(self):
        """Kamera değişkenlerini ve thread-safe (güvenli) depolamayı başlatır."""
        self.cap: Optional[cv2.VideoCapture] = None
        self.running: bool = False
        self._frame: Optional[np.ndarray] = None
        self._lock: threading.Lock = threading.Lock()
        self._thread: Optional[threading.Thread] = None

    def start(self) -> bool:
        """Kamera akışını ayrı bir arka plan thread'inde başlatır."""
        if self.running:
            return True

        self.cap = cv2.VideoCapture(CAMERA_INDEX)
        self.cap = cv2.VideoCapture(CAMERA_INDEX)
        if not self.cap or not self.cap.isOpened():
            # Burası önemli: Eğer kamera açılmazsa False dönmeli veya hata fırlatmalı
            return False
        if not self.cap.isOpened():
            raise RuntimeError(
                f"Kamera {CAMERA_INDEX} açılamadı. "
                "Bağlı olduğundan veya başka bir uygulama tarafından kullanılmadığından emin olun."
            )

        # Standart çözünürlük ayarları
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        self.running = True
        self._thread = threading.Thread(
            target=self._capture_loop,
            daemon=True,
            name="CameraThread"
        )
        self._thread.start()
        return True

    def stop(self) -> None:
        """Kamera akışını durdurur ve kaynakları serbest bırakır."""
        self.running = False
        
        if self._thread:
            self._thread.join(timeout=2)
        
        with self._lock:
            if self.cap:
                self.cap.release()
            self.cap = None
            self._frame = None

    def get_frame(self) -> Optional[np.ndarray]:
        """En son yakalanan karenin bir kopyasını güvenli bir şekilde döndürür."""
        with self._lock:
            if self._frame is None:
                return None
            return self._frame.copy()

    def is_alive(self) -> bool:
        """Kamera thread'inin çalışıp çalışmadığını kontrol eder."""
        return self.running and self._thread is not None and self._thread.is_alive()

    def _capture_loop(self) -> None:
        """Kamera durdurulana kadar sürekli kare yakalar."""
        if self.cap is None:
            return

        while self.running:
            ret, frame = self.cap.read()
            
            if ret:
                with self._lock:
                    self._frame = frame
            else:
                # Bağlantı koptuğunda döngüden çık
                self.running = False
                break
"""
# --- TEST VE ÇALIŞTIRMA BLOĞU ---
if __name__ == "__main__":
    cam = CameraModule()
    print("Sistem başlatılıyor...")
    print("Çıkmak için görüntü penceresi üzerindeyken 'q' tuşuna basın.")
    
    if cam.start():
        try:
            while True:
                frame = cam.get_frame()
                
                if frame is not None:
                    # Canlı görüntüyü göster
                    cv2.imshow("VisionGuard AI - Canli Izleme", frame)
                
                # 'q' tuşuna basılırsa veya pencere kapatılırsa çık
                # waitKey(1) görüntünün tazelenmesi için şarttır
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    print("\nKapatma isteği alındı...")
                    break
                    
        except KeyboardInterrupt:
            print("\nProgram kullanıcı tarafından durduruldu (Ctrl+C).")
        except Exception as e:
            print(f"\nBeklenmedik bir hata: {e}")
        finally:
            # Kaynakları her zaman temizle
            cam.stop()
            cv2.destroyAllWindows()
            print("Kamera kapatıldı ve kaynaklar serbest bırakıldı.")
"""            