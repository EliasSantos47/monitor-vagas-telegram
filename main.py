import requests
import time
import os

# O código vai pegar os valores que você cadastrar no Railway
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def enviar_mensagem(texto):
    if not TOKEN or not CHAT_ID:
        print("❌ ERRO: TOKEN ou CHAT_ID não configurados nas variáveis do Railway!")
        return
    
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": texto}
    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            print("✅ Mensagem enviada com sucesso!")
        else:
            print(f"⚠️ Erro no Telegram: {response.text}")
    except Exception as e:
        print(f"🔥 Erro de conexão: {e}")

if __name__ == "__main__":
    print("🚀 Bot iniciado! Verificando configurações...")
    
    # Mensagem de teste ao ligar
    enviar_mensagem("🤖 Olá! Seu bot de vagas está OFICIALMENTE ATIVO no Railway!")

    # Loop infinito para manter o bot vivo
    while True:
        print("🔎 Monitorando vagas (Simulação ativa)...")
        # Aqui você pode colocar sua lógica de raspagem depois
        
        print("😴 Aguardando 1 hora para a próxima verificação...")
        time.sleep(3600)