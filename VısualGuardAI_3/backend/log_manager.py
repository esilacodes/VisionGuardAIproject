"""
Log Manager - Passwordlenmiş ve Sıkıştırılmış Loglar
Tüm sistem olaylarını güvenli şekilde kaydeder
"""

import os
import json
from datetime import datetime
from pathlib import Path
from backend.encryption import encryption_manager

# Proje kök dizini (backend/ klasörünün üstü)
PROJECT_ROOT = Path(__file__).parent.parent

class LogManager:
    """Passwordlenmiş log yönetimi"""
    
    def __init__(self, log_dir="logs"):
        """
        Log yöneticisini başlat
        
        Args:
            log_dir: Log dosyaları dizini
        """
        self.log_dir = PROJECT_ROOT / log_dir
        self.log_dir.mkdir(exist_ok=True)
        
        # Log dosyaları
        self.motion_log = self.log_dir / "motion_detections.json"
        self.notification_log = self.log_dir / "notifications.json"
        self.user_log = self.log_dir / "user_activities.json"
        self.system_log = self.log_dir / "system_events.json"
        
        # Passwordlenmiş log dosyaları
        self.encrypted_motion_log = self.log_dir / "motion_detections.enc"
        self.encrypted_notification_log = self.log_dir / "notifications.enc"
        self.encrypted_user_log = self.log_dir / "user_activities.enc"
        self.encrypted_system_log = self.log_dir / "system_events.enc"
    
    def _get_timestamp(self):
        """Şu anki timestamp'i al"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    
    def log_motion_detection(self, detection_id, username, sensitivity=70):
        """
        Motion tespit edildiğini logla
        
        Args:
            detection_id: Tespit ID
            username: User adı
            sensitivity: Sensitivity değeri
        """
        log_entry = {
            "timestamp": self._get_timestamp(),
            "event_type": "motion_detected",
            "detection_id": detection_id,
            "username": username,
            "sensitivity": sensitivity,
            "status": "success"
        }
        
        self._append_log(self.motion_log, log_entry)
        self._save_encrypted_log(self.motion_log, self.encrypted_motion_log)
        
        print(f"📝 Motion log: Detection #{detection_id} ({username})")
    
    def log_notification_sent(self, notification_id, detection_id, username, message):
        """
        Notification gönderildiğini logla
        
        Args:
            notification_id: Notification ID
            detection_id: Tespit ID
            username: User adı
            message: Notification metni
        """
        log_entry = {
            "timestamp": self._get_timestamp(),
            "event_type": "notification_sent",
            "notification_id": notification_id,
            "detection_id": detection_id,
            "username": username,
            "message": message,
            "status": "success"
        }
        
        self._append_log(self.notification_log, log_entry)
        self._save_encrypted_log(self.notification_log, self.encrypted_notification_log)
        
        print(f"🔔 Notification log: #{notification_id} → {username}")
    def log_system_event(self, event_type, message, error=None, username=None):
        """
        Sistem olayını logla
        
        Args:
            event_type: Olay tipi (error, warning, info)
            message: Mesaj
            error: Error detayları (optional)
            username: User adı (optional)
        """
        log_entry = {
            "timestamp": self._get_timestamp(),
            "event_type": event_type,
            "message": message,
            "username": username,
            "error": str(error) if error else None,
            "status": "logged"
        }
        
        self._append_log(self.system_log, log_entry)
        self._save_encrypted_log(self.system_log, self.encrypted_system_log)
        
        level = "⚠️ " if event_type == "error" else "ℹ️ "
        print(f"{level}System log: {event_type} - {message}")
    
    def _append_log(self, log_file, entry):
        """
        JSON log dosyasına giriş ekle
        
        Args:
            log_file: Log dosyası yolu
            entry: Eklenecek giriş (dict)
        """
        try:
            # Dosya varsa oku
            if log_file.exists():
                with open(log_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
            else:
                logs = []
            
            # Login ekle
            logs.append(entry)
            
            # Geri yaz
            with open(log_file, 'w', encoding='utf-8') as f:
                json.dump(logs, f, ensure_ascii=False, indent=2)
        
        except Exception as e:
            print(f"❌ Log yazma hatası: {e}")
    
    def _save_encrypted_log(self, json_file, enc_file):
        """
        JSON log'u AES + LZMA ile şifrele ve kaydet
        
        Args:
            json_file: JSON log dosyası
            enc_file: Passwordlenmiş log dosyası
        """
        try:
            # JSON dosyasını oku
            if json_file.exists():
                with open(json_file, 'rb') as f:
                    json_data = f.read()
                
                # Passwordle
                encrypted_dict = encryption_manager.encrypt_log(json_data.decode('utf-8'))
                
                if encrypted_dict:
                    # Passwordlenmiş veriyi kaydet
                    with open(enc_file, 'w', encoding='utf-8') as f:
                        json.dump(encrypted_dict, f)
                    
                    original_size = len(json_data)
                    encrypted_size = len(str(encrypted_dict).encode())
                    compression = encryption_manager.get_compression_ratio(
                        original_size, 
                        encrypted_size
                    )
                    
                    print(f"🔐 Encrypted: {original_size} → {encrypted_size} bytes ({compression}% tasarruf)")
        
        except Exception as e:
            print(f"❌ Passwordleme hatası: {e}")
    
    def read_encrypted_log(self, enc_file):
        """
        Passwordlenmiş log'u oku ve şifresini çöz
        
        Args:
            enc_file: Passwordlenmiş log dosyası yolu
        
        Returns:
            Log girdileri (list) veya None
        """
        try:
            if not Path(enc_file).exists():
                return None
            
            # Passwordlenmiş veriyi oku
            with open(enc_file, 'r', encoding='utf-8') as f:
                encrypted_dict = json.load(f)
            
            # Passwordsini çöz
            decrypted_text = encryption_manager.decrypt_log(encrypted_dict)
            
            if decrypted_text:
                # JSON parse et
                logs = json.loads(decrypted_text)
                return logs
            
            return None
        
        except Exception as e:
            print(f"❌ Log okuma hatası: {e}")
            return None
    
    def get_motion_logs(self):
        """Tüm hareket tespit loglarını al"""
        return self.read_encrypted_log(self.encrypted_motion_log)
    
    def get_notification_logs(self):
        """Tüm bildirim loglarını al"""
        return self.read_encrypted_log(self.encrypted_notification_log)
    
    def get_user_logs(self):
        """Tüm kullanıcı aktivite loglarını al"""
        return self.read_encrypted_log(self.encrypted_user_log)
    
    def get_system_logs(self):
        """Tüm sistem olayı loglarını al (doğrudan JSON'dan oku)"""
        try:
            if self.system_log.exists():
                with open(self.system_log, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"❌ System log okuma hatası: {e}")
            return []

# Global instance
log_manager = LogManager()
