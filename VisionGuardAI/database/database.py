import sqlite3

class DatabaseManager:
    def __init__(self, db_name='users.db'):
        self.db_name = db_name
        self.create_table()
    
    def create_table(self):
        """Kullanıcı tablosunu oluştur"""
        baglanti = sqlite3.connect(self.db_name)
        cursor = baglanti.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        
        baglanti.commit()
        baglanti.close()
    
    
    def user_exists(self, username):
        
        baglanti = sqlite3.connect(self.db_name)
        cursor = baglanti.cursor()
        
        cursor.execute('SELECT * FROM users WHERE username=?', (username,))
        result = cursor.fetchone()
        
        baglanti.close()
        return result is not None
    
    def check_credentials(self, username, password):
        
        baglanti = sqlite3.connect(self.db_name)
        cursor = baglanti.cursor()
        
        cursor.execute('SELECT * FROM users WHERE username=? AND password=?', 
                      (username, password))
        result = cursor.fetchone()
        
        baglanti.close()
        return result is not None
    
    def add_user(self, username, password):
        
        baglanti = sqlite3.connect(self.db_name)
        cursor = baglanti.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO users (username, password)
                VALUES (?, ?)
            ''', (username, password))
            baglanti.commit()
            baglanti.close()
            return True
        except sqlite3.IntegrityError:
            baglanti.close()
            return False

    