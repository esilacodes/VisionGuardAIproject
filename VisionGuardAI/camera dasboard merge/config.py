# config.py
# ============================================
# SABIT DEĞERLER (Tüm program tarafından kullanılacak)
# ============================================
# CONSTANT VALUES (To be used throughout the entire program)
# ============================================

#window setting 
# PENCERE AYARLARI
WINDOW_WIDTH = 1500      # Pencere genişliği (pixel)
WINDOW_HEIGHT = 1000     # Pencere yüksekliği (pixel)
WINDOW_TITLE = "Motion Detection System"  # Pencere başlığı
BG_COLOR = "#f0f0f0"    # Arka plan rengi (hex format)

# colors 
# RENKLER
BUTTON_COLOR = "#4CAF50"      # Buton rengi (yeşil)
BUTTON_TEXT_COLOR = "white"   # Buton yazı rengi (beyaz)
BUTTON_HOVER_COLOR = "#45a049"  # Buton hover rengi
ERROR_COLOR = "#FF5252"       # Hata mesajı rengi (kırmızı)
SUCCESS_COLOR = "#4CAF50"     # Başarı mesajı rengi (yeşil)
INPUT_BG_COLOR = "white"      # Giriş alanı rengi (beyaz)
LABEL_COLOR = "#333333"       # Etiket rengi (koyu gri)

#widget setting 
# UI BOYUTLARI
BUTTON_WIDTH = 15             # Buton genişliği (karakter sayısı)
BUTTON_HEIGHT = 2             # Buton yüksekliği (satır sayısı)
ENTRY_WIDTH = 30              # Giriş alanı genişliği
LABEL_FONT = ("Arial", 10)    # Etiket fontu (isim, boyut)
TITLE_FONT = ("Arial", 14, "bold")  # Başlık fontu (isim, boyut, stil)
BUTTON_FONT = ("Arial", 11)   # Buton fontu

#valid users
# GEÇERLİ KULLANICILAR (username: password)
VALID_USERS = {
   "admin": "1234",
    "user": "password",
    "test": "test123",
    "ali":"12345"
    
}

# error message 
# HATA MESAJLARI
ERROR_EMPTY_USERNAME = "Username field cannot be empty!"
ERROR_EMPTY_PASSWORD = "Password field cannot be empty!"
ERROR_INVALID_CREDENTIALS = "Username or password is incorrect!"
ERROR_SHORT_USERNAME = "Username must be at least 3 characters!"
ERROR_SHORT_PASSWORD = "Password must be at least 4 characters!"

# SUCCESS MESSAGES
SUCCESS_LOGIN = "Login successful!"




####esladan gelen 
import os
from dotenv import load_dotenv

load_dotenv()

# Kamera indeksi: 0 (dahili), 1 veya 2 (harici USB)
CAMERA_INDEX = 0 

# İleride kullanacağın diğer ayarlar buraya gelecek
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")