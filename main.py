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
    return "Bot de Vagas Online - Ciclo 60min", 200

CARGOS = ["maitre", "gerente de aeb", "supervisor de restaurante", "chefe de bar", "coordenador de alimentos e bebidas"]
ESTADOS = ["São Paulo", "Bahia", "Minas Gerais", "Ceara", "Pernambuco", "Goias"]

def buscar_vagas_reais(cargo, estado):
    try:
        params = {
            "q": f"vagas {cargo} em {estado}",
            "engine": "google_jobs",
            "api_key": SERPAPI_KEY,
            "hl": "pt-br"
        }
        search = GoogleSearch(params)
        return search.get_dict().get("jobs_results", [])
    except Exception as e:
        print(f"Erro na API: {e}")
        return []

def monitor_vagas():
    bot.send_message(CHAT_ID, "🕒 **Configuração Atualizada!**\nO bot agora fará varreduras a cada **60 minutos**.")
    
    while True:
        # Ajuste de Horário (Brasília costuma ser -3h em relação ao servidor)
        agora = datetime.now() - timedelta(hours=3)
        proxima = agora + timedelta(minutes=60)
        
        cargo_da_vez = random.choice(CARGOS)
        estado_da_vez = random.choice(ESTADOS)
        
        print(f"[{agora.strftime('%H:%M:%S')}] Iniciando busca: {cargo_da_vez} em {estado_da_vez}")
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

        # Relatório de Status (Agora configurado para 60 min)
        status = f"✅ {vagas_enviadas} encontradas" if vagas_enviadas > 0 else "ℹ️ Sem vagas novas"
        relatorio = (
            f"📊 **RELATÓRIO DE VARREDURA (60min)**\n"
            f"⏰ Horário: {agora.strftime('%H:%M:%S')}\n"
            f"🔎 Busca: {cargo_da_vez} / {estado_da_vez}\n"
            f"📝 Status: {status}\n\n"
            f"⏭️ **Próxima pesquisa às: {proxima.strftime('%H:%M:%S')}**"
        )
        
        bot.send_message(CHAT_ID, relatorio, parse_mode="Markdown")
        
        # Espera 3600 segundos (60 minutos)
        print(f"Aguardando 60 minutos... Próxima às {proxima.strftime('%H:%M:%S')}")
        time.sleep(3600)

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    t = threading.Thread(target=monitor_vagas)
    t.start()
    run_flask()