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

# --- 1. FUNÇÃO DE BOAS-VINDAS PERSONALIZADA ---
@bot.message_handler(content_types=['new_chat_members'])
def boas_vindas(message):
    for novo_membro in message.new_chat_members:
        # Tenta pegar o sobrenome, se não existir, usa o primeiro nome
        nome_exibicao = novo_membro.last_name if novo_membro.last_name else novo_membro.first_name
        
        texto = (
            f"🎯 **Bem-vindo, {nome_exibicao}!**\n\n"
            "Canal exclusivo para vagas de gestão em restaurantes:\n"
            "🎩 Maitre | 📊 Gerente | 👔 Coordenador | 👁️ Supervisor\n\n"
            "🔔 **Ative as notificações para receber as oportunidades!**\n"
            "📩 Envio de vagas: a cada 1 hora, nos ajude a melhorar o filtro (envie msg com a sugestão no chat)"
        )
        bot.send_message(message.chat.id, texto, parse_mode="Markdown")

# --- 2. SERVIDOR WEB (KEEP-ALIVE) ---
@app.route('/')
def home():
    return "Bot Online: Vagas + Boas-Vindas Personalizado", 200

# --- 3. MONITORAMENTO DE VAGAS ---
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
        proxima = agora + timedelta(minutes=60)
        
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

        relatorio = (f"📊 **RELATÓRIO DE VARREDURA (60min)**\n⏰ {agora.strftime('%H:%M:%S')}\n🔎 {cargo_da_vez} / {estado_da_vez}\n"
                     f"📝 Status: {vagas_enviadas} encontradas\n\n⏭️ **Próxima: {proxima.strftime('%H:%M:%S')}**")
        bot.send_message(CHAT_ID, relatorio, parse_mode="Markdown")
        time.sleep(3600)

# --- 4. EXECUÇÃO ---
if __name__ == "__main__":
    # Thread do monitor de vagas
    threading.Thread(target=monitor_vagas, daemon=True).start()
    
    # Thread do Boas-Vindas (polling)
    threading.Thread(target=bot.infinity_polling, daemon=True).start()
    
    # Flask (Principal)
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)