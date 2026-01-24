import requests
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT

def enviar(mensagem):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    payload = {
        "chat_id": TELEGRAM_CHAT,
        "text": mensagem,
        "parse_mode": "HTML"
    }

    response = requests.post(url, data=payload)

    print("STATUS:", response.status_code)
    print("RESPOSTA:", response.text)
