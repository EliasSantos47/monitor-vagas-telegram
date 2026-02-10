import os
import time
import random
import threading
from datetime import datetime, timedelta
from flask import Flask
from telebot import TeleBot
from serpapi import GoogleSearch

# --- CONFIGURAÇÃO DE AMBIENTE ---
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

bot = TeleBot(TOKEN)
app = Flask(__name__)

# --- 1. FUNÇÃO DE BOAS-VINDAS (TEXTO PERSONALIZADO) ---
@bot.message_handler(content_types=['new_chat_members'])
def boas_vindas(message):
    print(f"Detectado novo membro no chat {message.chat.id}") # Isso vai aparecer no log do Render
    try:
        for novo_membro in message.new_chat_members:
            # Pega o sobrenome ou primeiro nome
            usuario = novo_membro.last_name if novo_membro.last_name else novo_membro.first_name
            
            texto = (
                f"🎯 **Bem-vindo, {usuario}!**\n\n"
                "Canal exclusivo para vagas de gestão em restaurantes:\n"
                "🎩 Maitre | 📊 Gerente | 👔 Coordenador | 👁️ Supervisor\n\n"
                "🔔 **Ative as notificações para receber as oportunidades!**\n"
                "📩 Envio de vagas: a cada 1 hora, nos ajude a melhorar o filtro (envie msg com a sugestão no chat)"
            )
            bot.send_message(message.chat.id, texto, parse_mode="Markdown")
    except Exception as e:
        print(f"Erro ao enviar boas-vindas: {e}")

# --- 2. SERVIDOR WEB (KEEP-ALIVE PARA O RENDER) ---
@app.route('/')
def home():
    return "Bot Online: Vagas (60min) + Boas-Vindas", 200

# --- 3. MONITORAMENTO DE VAGAS ---
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
        print(f"Erro na API SerpApi: {e}")
        return []

def monitor_vagas():
    # Mensagem de log inicial
    print("Iniciando monitor de vagas...")
    
    while True:
        try:
            # Ajuste de Horário (Brasília -3h)
            agora = datetime.now() - timedelta(hours=3)
            proxima = agora + timedelta(minutes=60)
            
            cargo_da_vez = random.choice(CARGOS)
            estado_da_vez = random.choice(ESTADOS)
            
            vagas = buscar_vagas_reais(cargo_da_vez, estado_da_vez)
            vagas_enviadas = 0
            
            if vagas:
                # Envia no máximo 2 vagas por ciclo para economizar API
                for vaga in vagas[:2]:
                    titulo = vaga.get("title", "CARGO").upper()
                    empresa = vaga.get("company_name", "Empresa")
                    local = vaga.get("location", "Brasil")
                    links = vaga.get("apply_options", [])
                    link_direto = links[0].get("link") if links else vaga.get("related_links", [{}])[0].get("link", "https://google.com")
                    
                    bot.send_message(CHAT_ID, f"📍 **{titulo}**\n🏢 Empresa: {empresa}\n🌎 Local: {local}\n\n🔗 **CANDIDATURA:**\n{link_direto}")
                    vagas_enviadas += 1

            # Relatório de status a cada 60 min
            status = f"✅ {vagas_enviadas} encontradas" if vagas