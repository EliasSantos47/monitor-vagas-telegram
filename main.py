import os
import time
from telebot import TeleBot
from serpapi import GoogleSearch

# Configurações do Render
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

bot = TeleBot(TOKEN)

# Filtros que você definiu
CARGOS = ["maitre", "gerente de aeb", "supervisor de restaurante"]
ESTADOS = ["São Paulo", "Bahia", "Minas Gerais"]

def buscar_vagas_reais():
    # Buscando apenas o primeiro cargo e estado da lista para teste
    search = GoogleSearch({
        "q": f"vagas {CARGOS[0]} em {ESTADOS[0]}",
        "engine": "google_jobs",
        "api_key": SERPAPI_KEY
    })
    
    results = search.get_dict()
    return results.get("jobs_results", [])

def iniciar_monitoramento():
    bot.send_message(CHAT_ID, "🚀 **Monitor Pro A&B Iniciado!**\nBuscando links diretos e formatando Cards...")
    
    while True:
        vagas = buscar_vagas_reais()
        
        if vagas:
            for vaga in vagas[:3]: # Envia as 3 primeiras vagas encontradas
                titulo = vaga.get("title")
                empresa = vaga.get("company_name")
                local = vaga.get("location")
                link = vaga.get("related_links", [{}])[0].get("link", "#")
                
                # Montando o Card igual ao da foto
                card = (
                    f"📍 **{titulo.upper()} - {local.upper()}**\n"
                    f"🏢 **Empresa:** {empresa}\n"
                    f"🔗 [Candidatar-se via Google Jobs]({link})\n"
                    f"_Encontrado via Google Jobs_"
                )
                bot.send_message(CHAT_ID, card, parse_mode="Markdown")
        
        # Relatório de Status
        bot.send_message(CHAT_ID, f"📊 **Relatório:** {len(vagas)} vagas reais processadas.")
        time.sleep(3600) # Verifica a cada 1 hora

if __name__ == "__main__":
    iniciar_monitoramento()