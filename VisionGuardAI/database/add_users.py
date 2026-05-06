
from database import DatabaseManager

db = DatabaseManager()

# İlk kullanıcıları ekle
users = [
    ("admin", "1234"),
    ("user", "password"),
    ("test", "test123"),
    ("ali", "12345")
]

for username, password in users:
    if db.add_user(username, password):
        print(f"✓ {username} eklendi!")
    else:
        print(f"✗ {username} zaten var veya hata!")

