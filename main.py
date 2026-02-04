import os
import time
import random
import threading
from datetime import datetime, timedelta
from flask import Flask
from telebot import TeleBot
from serpapi import GoogleSearch

# --- CONFIGURAÇÃO ---
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

bot = TeleBot(TOKEN)
app = Flask(__name__)

# Rota para o Cron-job.org acessar e manter o bot vivo
@app.route('/')
def home():
    return "Bot de Vagas está Online!", 200

CARGOS = ["maitre", "gerente de aeb", "supervisor de restaurante", "chefe de bar", "coordenador de alimentos e bebidas"]
ESTADOS = ["São Paulo", "Bahia", "Minas Gerais", "Ceara", "Pernambuco", "Goias"]

def buscar_vagas_reais(cargo, estado):
    try:
        params = {"q": f"vagas {cargo} em {estado}", "engine": "google_jobs", "api_key": SERPAPI_KEY, "hl": "pt-br"}
        search = GoogleSearch(params)
        return search.get_dict().get("jobs_results", [])
    except Exception as e:
        print(f"Erro na API: {e}")
        return []

def monitor_vagas():
    while True:
        agora = datetime.now() - timedelta(hours=3)
        proxima = agora + timedelta(minutes=15)
        
        cargo_da_vez = random.choice(CARGOS)
        estado_da_vez = random.choice(ESTADOS)
        
        vagas = buscar_vagas_reais(cargo_da_vez, estado_da_vez)
        vagas_enviadas = 0
        
        if vagas:
            for vaga in vagas[:2]:
                titulo = vaga.get("title", "CARGO").upper()
                empresa = vaga.get("company_name", "Empresa")
                local = vaga.get("location", "Brasil")
                links = vaga.get("apply_options", [])
                link_direto = links[0].get("link") if links else vaga.get("related_links", [{}])[0].get("link", "https://google.com")

                bot.send_message(CHAT_ID, f"📍 **{titulo}**\n🏢 Empresa: {empresa}\n🌎 Local: {local}\n\n🔗 **CANDIDATURA:**\n{link_direto}")
                vagas_enviadas += 1

        # Relatório de 15 minutos
        status = f"✅ {vagas_enviadas} encontradas" if vagas_enviadas > 0 else "ℹ️ Sem vagas novas"
        relatorio = (f"📊 **RELATÓRIO DE VARREDURA**\n⏰ {agora.strftime('%H:%M:%S')}\n🔎 {cargo_da_vez} / {estado_da_vez}\n"
                     f"📝 {status}\n\n⏭️ **Próxima: {proxima.strftime('%H:%M:%S')}**")
        
        bot.send_message(CHAT_ID, relatorio, parse_mode="Markdown")
        time.sleep(900)

# Função para rodar o Flask
def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    # Inicia o monitor de vagas em uma thread separada
    t = threading.Thread(target=monitor_vagas)
    t.start()
    # Inicia o servidor Flask na thread principal
    run_flask()