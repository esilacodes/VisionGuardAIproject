"""
Encryption Module - AES + LZMA (Cryptography 48.0+ Uyumlu)
Fotoğrafları AES ile şifreler ve LZMA ile sıkıştırır
"""

import lzma
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf import pbkdf2
from cryptography.hazmat.backends import default_backend
import base64


class EncryptionManager:
    """AES şifreleme ve LZMA sıkıştırma"""
    
    def __init__(self, master_password="visionguard_secure_2024"):
        """
        Passwordleme yöneticisini başlat
        
        Args:
            master_password: Ana şifre (default: güvenli şifre)
        """
        self.master_password = master_password.encode()
        self.backend = default_backend()
    
    def _derive_key(self, salt=None):
        """
        PBKDF2 ile anahtar türet (Cryptography 48.0+ uyumlu)
        
        Args:
            salt: Tuz (opsiyonel, yoksa random üret)
        
        Returns:
            (anahtar, tuz) tuple
        """
        if salt is None:
            salt = os.urandom(16)
        
        try:
            # Cryptography 48.0+ için yeni API
            kdf_obj = pbkdf2.PBKDF2(
                algorithm=hashes.SHA256(),
                length=32,  # 256-bit key
                salt=salt,
                iterations=100000
            )
            key = kdf_obj.derive(self.master_password)
        except Exception as e:
            print(f"⚠️ PBKDF2 hata: {e}")
            # Fallback: basit hash kullan
            import hashlib
            hash_input = self.master_password + salt
            key = hashlib.sha256(hash_input).digest()
            # 256-bit (32 bytes) sağlayacak şekilde genişlet
            while len(key) < 32:
                key += hashlib.sha256(key + hash_input).digest()
            key = key[:32]
        
        return key, salt
    
    def compress_data(self, data):
        """
        LZMA ile verileri sıkıştır
        
        Args:
            data: Sıkıştırılacak veri (bytes)
        
        Returns:
            Sıkıştırılmış veri (bytes)
        """
        try:
            compressed = lzma.compress(data, preset=9)  # Maksimum sıkıştırma
            return compressed
        except Exception as e:
            print(f"⚠️ LZMA sıkıştırma hatası: {e}")
            return data
    
    def decompress_data(self, compressed_data):
        """
        LZMA sıkıştırmasını aç
        
        Args:
            compressed_data: Sıkıştırılmış veri (bytes)
        
        Returns:
            Orijinal veri (bytes)
        """
        try:
            decompressed = lzma.decompress(compressed_data)
            return decompressed
        except Exception as e:
            print(f"⚠️ LZMA açma hatası: {e}")
            return None
    
    def encrypt_image(self, image_data):
        """
        Fotoğrafı AES ile şifrele (LZMA sıkıştırmadan sonra)
        
        Args:
            image_data: Orijinal fotoğraf (bytes)
        
        Returns:
            {
                'encrypted': Passwordlenmiş veri (base64),
                'iv': IV (base64),
                'salt': Tuz (base64)
            }
        """
        try:
            # 1. LZMA sıkıştır
            compressed = self.compress_data(image_data)
            
            print(f"📊 Sıkıştırma: {len(image_data)} → {len(compressed)} bytes")
            
            # 2. AES anahtarı ve tuzu oluştur
            key, salt = self._derive_key()
            
            # 3. IV (Initialization Vector) oluştur
            iv = os.urandom(16)
            
            # 4. AES-256-CBC cipher oluştur
            cipher = Cipher(
                algorithms.AES(key),
                modes.CBC(iv),
                backend=self.backend
            )
            encryptor = cipher.encryptor()
            
            # 5. PKCS7 padding ekle
            padding_length = 16 - (len(compressed) % 16)
            padded_data = compressed + bytes([padding_length] * padding_length)
            
            # 6. Passwordle
            encrypted = encryptor.update(padded_data) + encryptor.finalize()
            
            print(f"🔐 Passwordleme: {len(compressed)} → {len(encrypted)} bytes")
            
            # 7. Base64 encode et
            return {
                'encrypted': base64.b64encode(encrypted).decode(),
                'iv': base64.b64encode(iv).decode(),
                'salt': base64.b64encode(salt).decode()
            }
        
        except Exception as e:
            print(f"❌ Passwordleme hatası: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def decrypt_image(self, encrypted_dict):
        """
        Passwordlenmiş fotoğrafı çöz
        
        Args:
            encrypted_dict: {
                'encrypted': Passwordlenmiş veri (base64),
                'iv': IV (base64),
                'salt': Tuz (base64)
            }
        
        Returns:
            Orijinal fotoğraf (bytes) veya None
        """
        try:
            # 1. Base64 decode et
            encrypted = base64.b64decode(encrypted_dict['encrypted'])
            iv = base64.b64decode(encrypted_dict['iv'])
            salt = base64.b64decode(encrypted_dict['salt'])
            
            # 2. AES anahtarını oluştur (aynı salt ile)
            key, _ = self._derive_key(salt)
            
            # 3. AES-256-CBC cipher oluştur
            cipher = Cipher(
                algorithms.AES(key),
                modes.CBC(iv),
                backend=self.backend
            )
            decryptor = cipher.decryptor()
            
            # 4. Passwordsini çöz
            padded_data = decryptor.update(encrypted) + decryptor.finalize()
            
            # 5. PKCS7 padding'i kaldır
            padding_length = padded_data[-1]
            compressed = padded_data[:-padding_length]
            
            print(f"🔓 Password çözüldü: {len(encrypted)} → {len(compressed)} bytes")
            
            # 6. LZMA sıkıştırmasını aç
            decompressed = self.decompress_data(compressed)
            
            if decompressed:
                print(f"📦 Sıkıştırma açıldı: {len(compressed)} → {len(decompressed)} bytes")
            
            return decompressed
        
        except Exception as e:
            print(f"❌ Password çözme hatası: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def encrypt_log(self, log_text):
        """
        Log dosyasını şifrele
        
        Args:
            log_text: Log metni (str)
        
        Returns:
            Passwordlenmiş log dict
        """
        return self.encrypt_image(log_text.encode())
    
    def decrypt_log(self, encrypted_dict):
        """
        Passwordlenmiş log'u çöz
        
        Args:
            encrypted_dict: Passwordlenmiş log dict
        
        Returns:
            Log metni (str)
        """
        decrypted = self.decrypt_image(encrypted_dict)
        if decrypted:
            return decrypted.decode('utf-8', errors='ignore')
        return None
    
    def get_compression_ratio(self, original_size, compressed_size):
        """Sıkıştırma oranını hesapla"""
        if original_size == 0:
            return 0
        ratio = (1 - compressed_size / original_size) * 100
        return round(ratio, 2)


# Global instance
encryption_manager = EncryptionManager()
