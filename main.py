import os
import time
from telebot import TeleBot
from serpapi import GoogleSearch

# Configurações do Render
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

bot = TeleBot(TOKEN)

# Suas listas completas (17 cargos e 11 estados)
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

def buscar_vagas_reais(cargo, estado):
    search = GoogleSearch({
        "q": f"vagas {cargo} em {estado}",
        "engine": "google_jobs",
        "api_key": SERPAPI_KEY
    })
    results = search.get_dict()
    return results.get("jobs_results", [])

def iniciar_monitoramento():
    bot.send_message(CHAT_ID, "🚀 **Monitor Pro A&B Iniciado!**\nLinks corrigidos e busca expandida para todos os estados.")
    
    while True:
        vagas_encontradas_total = 0
        
        # Para não gastar todos os seus créditos da SerpApi de uma vez, 
        # ele vai sortear 2 cargos e 2 estados por hora para verificar
        import random
        cargos_da_vez = random.sample(CARGOS, 2)
        estados_da_vez = random.sample(ESTADOS, 2)

        for cargo in cargos_da_vez:
            for estado in estados_da_vez:
                vagas = buscar_vagas_reais(cargo, estado)
                
                for vaga in vagas[:2]: # Pega as 2 melhores de cada combinação
                    titulo = vaga.get("title", "Cargo não informado")
                    empresa = vaga.get("company_name", "Empresa não informada")
                    local = vaga.get("location", "Localização não informada")
                    
                    # CORREÇÃO DO LINK: Pegamos o link direto de candidatura
                    link_candidatura = vaga.get("related_links", [{}])[0].get("link")
                    
                    if link_candidatura:
                        card = (
                            f"📍 **{titulo.upper()}**\n"
                            f"🏢 **Empresa:** {empresa}\n"
                            f"🌎 **Local:** {local}\n\n"
                            f"🔗 **LINK PARA CANDIDATURA:**\n{link_candidatura}\n"
                            f"---"
                        )
                        bot.send_message(CHAT_ID, card, parse_mode="Markdown")
                        vagas_encontradas_total += 1
        
        bot.send_message(CHAT_ID, f"📊 **Relatório:** {vagas_encontradas_total} novas vagas reais enviadas.")
        time.sleep(3600) # Aguarda 1 hora

if __name__ == "__main__":
    iniciar_monitoramento()