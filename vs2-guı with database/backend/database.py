
import sqlite3
import hashlib
from pathlib import Path

class Database:
    def __init__(self, db_name="motion_detection.db"):
        self.db_path = Path(db_name)
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
        
        conn.commit()
        conn.close()
    
    def hash_password(self, password):
        """Şifre hash'le"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self, username, email, password):
        """Kullanıcı kaydet"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Validasyon
            if len(password) < 6:
                return False, "Password must be at least 6 characters long."
#" "Şifre en az 6 karakter olmalıdır"
            
            hashed_password = self.hash_password(password)
            
            cursor.execute('''
                INSERT INTO users (username, email, password)
                VALUES (?, ?, ?)
            ''', (username, email, hashed_password))
            
            conn.commit()
            conn.close()
            return True, "Registration successful! You can now log in."#"Kayıt başarılı! Giriş yapabilirsiniz."
        
        except sqlite3.IntegrityError as e:
            if "username" in str(e):
                return False, "This username is already in use."#"Bu kullanıcı adı zaten kullanılıyor"
            elif "email" in str(e):
                return False, "This email is already registered."
#"Bu e-posta zaten kayıtlı"
            return False, "An error occurred during registration."#"Kayıt sırasında hata oluştu"
        
        except Exception as e:
            return False, f"Hata: {str(e)}"
    
    def login_user(self, username, password):
        """Kullanıcı giriş"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Validasyon
            if not username or not password:
                return False, "Username and password are required."
#"Kullanıcı adı ve şifre gereklidir"
            
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
#"Kullanıcı adı veya şifre hatalı"
        
        except Exception as e:
            return False, f"Giriş sırasında hata oluştu"
    
    def set_current_user(self, username):
        """Giriş yapan kullanıcıyı ayarla"""
        self.current_user = username
    
    def get_current_user(self):
        """Giriş yapan kullanıcıyı al"""
        return self.current_user
    
    def logout(self):
        """Çıkış yap"""
        self.current_user = None
    
    def change_username(self, new_username):
        """Kullanıcı adını değiştir"""
        try:
            if not self.current_user:
                return False, "You are not logged in."
#"Giriş yapmamışsınız"
            
            if not new_username or len(new_username) < 3:
                return False, "Username must be at least 3 characters long."
#"Kullanıcı adı en az 3 karakter olmalıdır"
            
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
#"Kullanıcı adı başarıyla değiştirildi"
        
        except sqlite3.IntegrityError:
            return False, "This username is already in use."
#"Bu kullanıcı adı zaten kullanılıyor"
        except Exception as e:
            return False, f"Hata: {str(e)}"
    
    def change_password(self, old_password, new_password):
        """Şifreyi değiştir"""
        try:
            if not self.current_user:
                return False, "You are not logged in."#"Giriş yapmamışsınız"
            
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
# "Eski şifre hatalı"
            
            # Yeni şifreyi kaydet
            new_hashed = self.hash_password(new_password)
            cursor.execute('''
                UPDATE users SET password = ?
                WHERE username = ?
            ''', (new_hashed, self.current_user))
            
            conn.commit()
            conn.close()
            return True, "Password changed successfully."
#"Şifre başarıyla değiştirildi"
        
        except Exception as e:
            return False, f"Hata: {str(e)}"
    
    def delete_account(self, password):
        """Hesabı sil"""
        try:
            if not self.current_user:
                return False,"You are not logged in."# "Giriş yapmamışsınız"
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            hashed_password = self.hash_password(password)
            
            # Şifreyi kontrol et
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
            return False, f"Hata: {str(e)}"

# Global database instance
db = Database()