
import sqlite3
import hashlib
from pathlib import Path
import json
from backend.encryption import encryption_manager

# Proje kök dizini (backend/ klasörünün üstü)
PROJECT_ROOT = Path(__file__).parent.parent

class Database:
    def __init__(self, db_name="motion_detection.db"):
        self.db_path = PROJECT_ROOT / db_name
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.current_user = None
        self.init_database()
    
    def init_database(self):
        """Veritabanını başlat"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Users tablosu
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
               email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Detections tablosu (fotoğraflar)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS detections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                image_data BLOB,
                is_encrypted INTEGER DEFAULT 1,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (username) REFERENCES users(username)
            )
        ''')
        
        # Notifications tablosu (bildirimler)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                detection_id INTEGER,
                message TEXT,
                sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (username) REFERENCES users(username),
                FOREIGN KEY (detection_id) REFERENCES detections(id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def hash_password(self, password):
        """Password hash'le"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self, username, email, password):
        """User kaydet"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Validasyon
            if len(password) < 6:
                return False, "Password must be at least 6 characters long."
#" "Password en az 6 karakter olmalıdır"
            
            hashed_password = self.hash_password(password)
            
            cursor.execute('''
                INSERT INTO users (username, email, password)
                VALUES (?, ?, ?)
            ''', (username, email, hashed_password))
            
            conn.commit()
            conn.close()
            return True, "Registration successful! You can now log in."#"Record başarılı! Login yapabilirsiniz."
        
        except sqlite3.IntegrityError as e:
            if "username" in str(e):
                return False, "This username is already in use."#"Bu kullanıcı adı zaten kullanılıyor"
            elif "email" in str(e):
                return False, "This email is already registered."
#"Bu e-posta zaten kayıtlı"
            return False, "An error occurred during registration."#"Record sırasında hata oluştu"
        
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def login_user(self, username, password):
        """User giriş"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Validasyon
            if not username or not password:
                return False, "Username and password are required."
#"User adı ve şifre gereklidir"
            
            hashed_password = self.hash_password(password)
            
            cursor.execute('''
                SELECT id, username, email FROM users
                WHERE username = ? AND password = ?
            ''', (username, hashed_password))
            
            user = cursor.fetchone()
            conn.close()
            
            if user:
                return True, f"welcome, {user[1]}!"
            else:
                return False, "Incorrect username or password."
        
        except Exception as e:
            return False, "An error occurred during login."
    
    def set_current_user(self, username):
        """Login yapan kullanıcıyı ayarla"""
        self.current_user = username
    def logout(self):
        """Logout yap"""
        self.current_user = None
    
    def change_username(self, new_username):
        """User adını değiştir"""
        try:
            if not self.current_user:
                return False, "You are not logged in."
#"Login yapmamışsınız"
            
            if not new_username or len(new_username) < 3:
                return False, "Username must be at least 3 characters long."
#"User adı en az 3 karakter olmalıdır"
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE users SET username = ?
                WHERE username = ?
            ''', (new_username, self.current_user))
            
            conn.commit()
            conn.close()
            
            self.current_user = new_username
            return True, "Username changed successfully."
#"User adı başarıyla değiştirildi"
        
        except sqlite3.IntegrityError:
            return False, "This username is already in use."
#"Bu kullanıcı adı zaten kullanılıyor"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def change_password(self, old_password, new_password):
        """Passwordyi değiştir"""
        try:
            if not self.current_user:
                return False, "You are not logged in."#"Login yapmamışsınız"
            
            if len(new_password) < 6:
                return False, "New password must be at least 6 characters long."
#"Yeni şifre en az 6 karakter olmalıdır"
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            old_hashed = self.hash_password(old_password)
            
            # Eski şifreyi kontrol et
            cursor.execute('''
                SELECT id FROM users
                WHERE username = ? AND password = ?
            ''', (self.current_user, old_hashed))
            
            if not cursor.fetchone():
                conn.close()
                return False,"Old password is incorrect."
            
            # Yeni şifreyi kaydet
            new_hashed = self.hash_password(new_password)
            cursor.execute('''
                UPDATE users SET password = ?
                WHERE username = ?
            ''', (new_hashed, self.current_user))
            
            conn.commit()
            conn.close()
            return True, "Password changed successfully."
#"Password başarıyla değiştirildi"
        
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def delete_account(self, password):
        """Hesabı sil"""
        try:
            if not self.current_user:
                return False,"You are not logged in."# "Login yapmamışsınız"
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            hashed_password = self.hash_password(password)
            
            # Passwordyi kontrol et
            cursor.execute('''
                SELECT id FROM users
                WHERE username = ? AND password = ?
            ''', (self.current_user, hashed_password))
            
            if not cursor.fetchone():
                conn.close()
                return False, "password is wrong"
            
            # Hesabı sil
            cursor.execute('''
                DELETE FROM users WHERE username = ?
            ''', (self.current_user,))
            
            conn.commit()
            conn.close()
            
            self.current_user = None
            return True,"Account successfully deleted."
#" "Hesap başarıyla silindi"
        
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def save_detection(self, image_data, encrypt=True):
        """
        Tespit edilen fotoğrafı kaydet (AES + LZMA ile)
        
        Args:
            image_data: Fotoğraf (bytes)
            encrypt: Passwordleme aktif mi? (default: True)
        
        Returns:
            (Başarı, detection_id)
        """
        try:
            if not self.current_user:
                return False, None
            
            # Passwordleme varsa uygula
            if encrypt:
                encrypted_dict = encryption_manager.encrypt_image(image_data)
                if encrypted_dict:
                    # JSON formatında kaydet
                    storage_data = json.dumps(encrypted_dict).encode()
                    is_encrypted = True
                else:
                    storage_data = image_data
                    is_encrypted = False
            else:
                storage_data = image_data
                is_encrypted = False
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO detections (username, image_data, is_encrypted)
                VALUES (?, ?, ?)
            ''', (self.current_user, storage_data, is_encrypted))
            
            conn.commit()
            detection_id = cursor.lastrowid
            conn.close()
            
            return True, detection_id
        except Exception as e:
            print(f"save_detection hatası: {e}")
            return False, None
    
    def save_notification(self, detection_id, message):
        """Notificationi kaydet"""
        try:
            if not self.current_user:
                return False
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO notifications (username, detection_id, message)
                VALUES (?, ?, ?)
            ''', (self.current_user, detection_id, message))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            return False
    
    def get_detections(self, limit=100, username=None):
        """Tüm tespit edilen fotoğrafları al"""
        try:
            active_user = username or self.current_user
            if not active_user:
                return []
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, timestamp FROM detections
                WHERE username = ?
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (active_user, limit))
            
            results = cursor.fetchall()
            conn.close()
            return results
        except Exception as e:
            return []
    
    def get_detection_image(self, detection_id):
        """
        Tespit edilen fotoğrafı al (otomatik şifre çözme)
        
        Args:
            detection_id: Tespit ID
        
        Returns:
            Orijinal fotoğraf (bytes) veya None
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT image_data, is_encrypted FROM detections
                WHERE id = ?
            ''', (detection_id,))
            
            result = cursor.fetchone()
            conn.close()
            
            if not result:
                return None
            
            image_data, is_encrypted = result
            
            # Passwordlenmişse çöz
            if is_encrypted:
                try:
                    encrypted_dict = json.loads(image_data)
                    decrypted = encryption_manager.decrypt_image(encrypted_dict)
                    return decrypted
                except Exception as e:
                    print(f"Password çözme hatası: {e}")
                    return None
            else:
                return image_data
        
        except Exception as e:
            print(f"get_detection_image hatası: {e}")
            return None
    
    def get_notifications(self, limit=100, username=None):
        """Tüm bildirimleri al"""
        try:
            active_user = username or self.current_user
            if not active_user:
                return []
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, detection_id, message, sent_at FROM notifications
                WHERE username = ?
                ORDER BY sent_at DESC
                LIMIT ?
            ''', (active_user, limit))
            
            results = cursor.fetchall()
            conn.close()
            return results
        except Exception as e:
            return []

# Global database instance
db = Database()
