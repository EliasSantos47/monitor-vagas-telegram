import requests
from bs4 import BeautifulSoup
import time
import os

# --- CONFIGURAÇÕES (COLE SEUS DADOS AQUI) ---
TOKEN = "8293582725:AAFp6tviJ5rVd7fVvoP7kun1b7uORX_hyIk"
CHAT_ID = "@vagas_aeb_brail"

# Lista de sites para monitorar (Exemplo simples para teste)
# Você pode adicionar as URLs reais de busca do InfoJobs/Gupy aqui
SITES = [
    {"nome": "InfoJobs - Exemplo", "url": "https://www.infojobs.com.br/vagas-de-emprego.aspx"},
]

VAGAS_ENVIADAS = set()

def enviar_mensagem(texto):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": texto}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print(f"Erro ao enviar Telegram: {e}")

def monitorar():
    print("🔎 Iniciando ronda de vagas...")
    for site in SITES:
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(site['url'], headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Aqui vai a lógica de busca de títulos (simplificada para não dar erro)
            # Ele vai apenas avisar que acessou o site com sucesso no primeiro teste
            enviar_mensagem(f"✅ Monitorando: {site['nome']}\nO robô está ativo e procurando!")
            
        except Exception as e:
            print(f"Erro ao acessar {site['nome']}: {e}")

# LOOP PRINCIPAL (IMORTAL)
if __name__ == "__main__":
    enviar_mensagem("🚀 Bot de Vagas Iniciado com Sucesso no Railway!")
    while True:
        monitorar()
        print("😴 Dormindo por 30 minutos...")
        time.sleep(1800) # Espera 30 minutos
