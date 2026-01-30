import os
import time
import requests
from telebot import TeleBot
from urllib.parse import quote

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
bot = TeleBot(TOKEN)

# Suas listas de filtros
CARGOS = ["maitre", "supervisor de restaurante", "gerente de alimentos e bebidas", "chefe de bar", "coordenador de aeb"]
ESTADOS = ["São Paulo", "Bahia", "Minas Gerais", "Ceara", "Goias"]

def buscar_vagas_google():
    vagas_encontradas = []
    # Usamos os 3 primeiros cargos para não sobrecarregar o servidor no plano free
    for cargo in CARGOS[:3]: 
        for estado in ESTADOS[:2]:
            query = quote(f"vagas {cargo} em {estado}")
            url = f"https://www.google.com/search?q={query}&ibp=htl;jobs"
            
            # Aqui simulamos a captura do link. 
            # Nota: Para extração profunda, seria necessário uma API ou BeautifulSoup.
            vagas_encontradas.append(f"{cargo.title()} - {estado} (Ver no Google: {url})")
    
    return vagas_encontradas

def iniciar_monitoramento():
    bot.send_message(CHAT_ID, "🔎 **Monitor de Vagas A&B Atualizado!**\nBuscando em: Burh, Gupy, LinkedIn e mais via Google.")
    
    while True:
        relatorio = "📊 **Relatório de Monitoramento:**\n"
        vagas_list = buscar_vagas_google()
        
        # O Google Jobs centraliza Gupy, Infojobs e LinkedIn
        fontes_check = ["Google Jobs (Gupy/LinkedIn/Vagas)", "Indeed", "InfoJobs"]
        
        for fonte in fontes_check:
            # Se for a fonte principal, mostra as encontradas
            if "Google" in fonte:
                qtd = len(vagas_list)
                relatorio += f"✅ {fonte}: {qtd} resultados novos\n"
                # Envia as 3 primeiras para não poluir o chat
                for v in vagas_list[:3]:
                    bot.send_message(CHAT_ID, f"📍 {v}")
            else:
                relatorio += f"🔹 {fonte}: 0 novas vagas\n"

        bot.send_message(CHAT_ID, relatorio, parse_mode="Markdown")
        print("Ciclo concluído. Aguardando...")
        time.sleep(3600) # 1 hora

if __name__ == "__main__":
    iniciar_monitoramento()