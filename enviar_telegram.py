import requests
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT

def enviar(msg):
    print("TOKEN:", TELEGRAM_TOKEN)
    print("CHAT:", TELEGRAM_CHAT)

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    payload = {
        "chat_id": TELEGRAM_CHAT,
        "text": msg
    }

    r = requests.post(url, data=payload)
    print("STATUS:", r.status_code)
    print("RESPOSTA:", r.text)

