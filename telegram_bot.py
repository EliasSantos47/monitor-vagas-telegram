import requests
import time
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

def enviar_telegram(mensagem: str):
    """Envia a mensagem formatada para o canal do Telegram via API"""
    
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("❌ ERRO: TELEGRAM_TOKEN ou TELEGRAM_CHAT_ID não definidos nas configurações.")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    payload = {
        "chat_id": str(TELEGRAM_CHAT_ID),
        "text": mensagem,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }

    # Tentativas de reenvio em caso de falha de conexão (Network Flapping)
    tentativas = 3
    for i in range(tentativas):
        try:
            response = requests.post(url, data=payload, timeout=20)
            
            if response.status_code == 200:
                print(f"✅ Notificação enviada com sucesso! (Código: {response.status_code})")
                return True
            else:
                print(f"⚠️ Telegram retornou erro {response.status_code}: {response.text}")
                break # Se o erro for do Telegram (ex: Chat ID errado), não adianta tentar de novo
                
        except (requests.exceptions.RequestException, Exception) as e:
            print(f"❌ Tentativa {i+1}/{tentativas} falhou: {e}")
            if i < tentativas - 1:
                time.sleep(5) # Espera 5 segundos antes de tentar de novo
            else:
                print("🚨 Todas as tentativas de envio ao Telegram falharam.")
    
    return False