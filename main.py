import os
import time
import random
from datetime import datetime, timedelta
from telebot import TeleBot
from serpapi import GoogleSearch

# Configurações do Render
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

bot = TeleBot(TOKEN)

# Filtros
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
        results = search.get_dict()
        return results.get("jobs_results", [])
    except Exception as e:
        print(f"Erro na API: {e}")
        return []

def iniciar_monitoramento():
    bot.send_message(CHAT_ID, "✅ **Sistema de Monitoramento 15min Ativo!**\nO bot agora enviará relatórios constantes.")
    
    while True:
        agora = datetime.now() - timedelta(hours=3) # Ajuste para horário de Brasília se necessário
        proxima = agora + timedelta(minutes=15)
        
        cargo_da_vez = random.choice(CARGOS)
        estado_da_vez = random.choice(ESTADOS)
        
        print(f"[{agora.strftime('%H:%M:%S')}] Iniciando busca: {cargo_da_vez} em {estado_da_vez}")
        vagas = buscar_vagas_reais(cargo_da_vez, estado_da_vez)
        
        vagas_enviadas = 0
        if vagas:
            for vaga in vagas[:2]:
                titulo = vaga.get("title", "CARGO").upper()
                empresa = vaga.get("company_name", "Empresa não informada")
                local = vaga.get("location", "Brasil")
                links_lista = vaga.get("apply_options", [])
                link_direto = links_lista[0].get("link") if links_lista else vaga.get("related_links", [{}])[0].get("link", "https://google.com")

                card = (
                    f"📍 **{titulo}**\n"
                    f"🏢 Empresa: {empresa}\n"
                    f"🌎 Local: {local}\n\n"
                    f"🔗 **LINK PARA CANDIDATURA:**\n"
                    f"{link_direto}"
                )
                bot.send_message(CHAT_ID, card)
                vagas_enviadas += 1

        # RELATÓRIO DE VARREDURA (A cada 15 min)
        status_vagas = f"✅ {vagas_enviadas} novas encontradas" if vagas_enviadas > 0 else "ℹ️ Nenhuma vaga nova nesta rodada"
        
        relatorio = (
            f"📊 **RELATÓRIO DE VARREDURA**\n"
            f"⏰ Horário: {agora.strftime('%H:%M:%S')}\n"
            f"🔎 Busca: {cargo_da_vez} / {estado_da_vez}\n"
            f"📝 Status: {status_vagas}\n\n"
            f"⏭️ **Próxima pesquisa às: {proxima.strftime('%H:%M:%S')}**"
        )
        
        bot.send_message(CHAT_ID, relatorio, parse_mode="Markdown")
        
        print(f"Aguardando 15 minutos... Próxima às {proxima.strftime('%H:%M:%S')}")
        time.sleep(900) # 900 segundos = 15 minutos

if __name__ == "__main__":
    iniciar_monitoramento()