
import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def send_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": text})
    except:
        pass
