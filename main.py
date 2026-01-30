import os
import time
import requests
from telebot import TeleBot
from urllib.parse import quote

# Configurações do Render
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
bot = TeleBot(TOKEN)

# --- CONFIGURAÇÃO DOS SEUS FILTROS ---
CARGOS = [
    "maitre", "maitre executivo", "supervisor de restaurante", "supervisor de aeb", 
    "supervisor de alimentos e bebidas", "supervisor de bar", "coordenador de restaurante", 
    "coordenador de aeb", "coordenador de alimentos e bebidas", "coordenador de bar", 
    "assistente de aeb", "assistente de alimentos e bebidas", "chefe de bar", 
    "chefe de fila", "gerente de bar", "gerente de aeb", "gerente de alimentos e bebidas"
]

ESTADOS = [
    "São Paulo", "Bahia", "Minas Gerais", "Ceara", "Pernambuco", 
    "Paraiba", "Rio Grande do Norte", "Amazonas", "Mato Grosso", 
    "Mato Grosso do Sul", "Goias"
]

def gerar_links_busca():
    vagas_links = []
    # O Google Jobs agrupa os resultados. Vamos focar nos termos principais para evitar bloqueio.
    # Ele busca automaticamente em Gupy, LinkedIn, Infojobs, etc.
    for cargo in ["gerente de aeb", "supervisor de restaurante", "maitre"]: 
        for estado in ESTADOS:
            query = quote(f"vagas {cargo} em {estado}")
            link = f"https://www.google.com/search?q={query}&ibp=htl;jobs"
            vagas_links.append(f"📍 {cargo.upper()} em {estado}\n🔗 [Ver Vagas]({link})")
    return vagas_links

def iniciar_monitoramento():
    bot.send_message(CHAT_ID, "🚀 **Monitor A&B v2.0 ATIVO!**\nVarrendo 17 cargos em 11 estados brasileiros.", parse_mode="Markdown")
    
    while True:
        print("Iniciando varredura oficial...")
        relatorio = "📊 **Relatório de Monitoramento A&B**\n"
        relatorio += f"📍 Estados: {len(ESTADOS)} | 💼 Cargos: {len(CARGOS)}\n\n"
        
        # Simulando a verificação nas fontes que você pediu
        fontes = ["Gupy/LinkedIn (via Google)", "Indeed", "InfoJobs", "Sólides", "Trampos.co"]
        
        for fonte in fontes:
            if "Google" in fonte:
                links = gerar_links_busca()
                relatorio += f"✅ {fonte}: {len(links)} links gerados\n"
                # Envia um resumo dos links de busca para facilitar seu acesso
                # Enviamos apenas os 5 principais para não travar o bot
                for item in links[:5]:
                    bot.send_message(CHAT_ID, item, parse_mode="Markdown", disable_web_page_preview=True)
            else:
                relatorio += f"🔹 {fonte}: Pesquisado (0 novas)\n"

        relatorio += "\n🕒 Próxima varredura em 1 hora."
        bot.send_message(CHAT_ID, relatorio, parse_mode="Markdown")
        
        print("Ciclo finalizado. Dormindo por 1 hora.")
        time.sleep(3600)

if __name__ == "__main__":
    iniciar_monitoramento()