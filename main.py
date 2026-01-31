import os
import time
import random
from telebot import TeleBot
from serpapi import GoogleSearch

# Variáveis de Ambiente
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

bot = TeleBot(TOKEN)

# Seus Filtros Reais
CARGOS = ["maitre", "gerente de aeb", "supervisor de restaurante", "chefe de bar"]
ESTADOS = ["São Paulo", "Bahia", "Minas Gerais", "Ceara", "Goias", "Pernambuco"]

def buscar_vagas(cargo, estado):
    try:
        params = {
            "q": f"vagas {cargo} em {estado}",
            "engine": "google_jobs",
            "api_key": SERPAPI_KEY
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        return results.get("jobs_results", [])
    except Exception as e:
        print(f"Erro na busca: {e}")
        return []

def iniciar_monitoramento():
    print("Bot iniciado. Aguardando conexão...")
    bot.send_message(CHAT_ID, "🚀 **Monitor Pro A&B Online!**\nVerificando chaves e links clicáveis...")
    
    while True:
        # Escolhe 1 cargo e 1 estado por vez para testar sem travar
        cargo_teste = random.choice(CARGOS)
        estado_teste = random.choice(ESTADOS)
        
        print(f"Buscando: {cargo_teste} em {estado_teste}")
        vagas = buscar_vagas(cargo_teste, estado_teste)
        
        if vagas:
            for vaga in vagas[:3]: # Envia as 3 melhores
                titulo = vaga.get("title", "Cargo").upper()
                empresa = vaga.get("company_name", "Empresa não informada")
                local = vaga.get("location", "Brasil")
                
                # Extração do Link Direto
                links = vaga.get("related_links", [])
                link_final = links[0].get("link") if links else "https://www.google.com/search?q=vagas+jobs"

                # Mensagem com Link Azul Automático (URL por extenso)
                mensagem = (
                    f"📍 **{titulo}**\n"
                    f"🏢 Empresa: {empresa}\n"
                    f"🌎 Local: {local}\n\n"
                    f"🔗 **LINK PARA CANDIDATURA:**\n"
                    f"{link_final}\n"
                    f"---"
                )
                bot.send_message(CHAT_ID, mensagem, parse_mode="Markdown")
        
        print("Ciclo completo. Dormindo 1 hora.")
        time.sleep(3600)

if __name__ == "__main__":
    iniciar_monitoramento()