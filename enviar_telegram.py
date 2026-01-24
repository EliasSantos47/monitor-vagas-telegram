import requests
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT

def enviar(mensagem):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    payload = {
        "chat_id": TELEGRAM_CHAT,
        "text": mensagem,
        "parse_mode": "HTML"
    }

    r = requests.post(url, json=payload)
    print("STATUS:", r.status_code)
    print("RESPOSTA:", r.text)

