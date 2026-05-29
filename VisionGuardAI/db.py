
import sqlite3
from cryptography.fernet import Fernet
import base64
import hashlib

class Database:
    def __init__(self, db_name="app.db"):
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()
        self._init()

        key = base64.urlsafe_b64encode(hashlib.sha256(b"secret_key").digest())
        self.cipher = Fernet(key)

    def _init(self):
        self.cur.execute('''
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT,
            telegram TEXT
        )
        ''')

        self.cur.execute('''
        CREATE TABLE IF NOT EXISTS logs(
            id INTEGER PRIMARY KEY,
            message TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        self.conn.commit()

    def encrypt(self, text):
        return self.cipher.encrypt(text.encode()).decode()

    def decrypt(self, text):
        return self.cipher.decrypt(text.encode()).decode()

    def add_user(self, username, password, telegram):
        try:
            self.cur.execute("SELECT * FROM users WHERE username=?", (username,))
            if self.cur.fetchone():
                return False, "User exists"

            self.cur.execute(
                "INSERT INTO users(username,password,telegram) VALUES(?,?,?)",
                (username, self.encrypt(password), telegram)
            )
            self.conn.commit()
            return True, "Registered"
        except Exception as e:
            return False, str(e)

    def login(self, username, password):
        self.cur.execute("SELECT password FROM users WHERE username=?", (username,))
        row = self.cur.fetchone()
        if not row:
            return False
        try:
            return self.decrypt(row[0]) == password
        except:
            return False
