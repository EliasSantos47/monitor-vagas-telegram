import os
import random
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

# Cargos de Gestão e Operacionais
CARGOS_GESTAO = ["maitre", "gerente de aeb", "supervisor de restaurante", "chefe de bar", "coordenador de alimentos e bebidas"]
CARGOS_MOGI = ["garçom", "garçonete"]
ESTADOS = ["São Paulo", "Bahia", "Minas Gerais", "Ceara", "Pernambuco", "Goias", "Rio de Janeiro", "Santa Catarina"]

def buscar_vagas_reais(cargo, localidade):
    try:
        params = {
            "q": f"vagas {cargo} em {localidade}",
            "engine": "google_jobs",
            "api_key": SERPAPI_KEY,
            "hl": "pt-br",
            "gl": "br"
        }
        search = GoogleSearch(params)
        results = search.get_dict().get("jobs_results", [])
        if results:
            random.shuffle(results) # Garante que não repita sempre as mesmas
        return results
    except Exception as e:
        print(f"Erro na SerpApi: {e}")
        return []

@app.route('/')
def executar_busca():
    agora = datetime.now() - timedelta(hours=3)
    
    # Lógica de sorteio: 30% de chance de buscar em Mogi, 70% nos cargos de gestão
    if random.random() < 0.3:
        cargo_da_vez = random.choice(CARGOS_MOGI)
        local_da_vez = "Mogi das Cruzes, SP"
    else:
        cargo_da_vez = random.choice(CARGOS_GESTAO)
        local_da_vez = random.choice(ESTADOS)
    
    vagas = buscar_vagas_reais(cargo_da_vez, local_da_vez)
    vagas_enviadas = 0
    
    if vagas:
        for vaga in vagas[:2]:
            titulo = vaga.get("title", "CARGO").upper()
            empresa = vaga.get("company_name", "Empresa")
            local = vaga.get("location", "Local")
            links = vaga.get("apply_options", [])
            link_direto = links[0].get("link") if links else "https://google.com"

            bot.send_message(CHAT_ID, f"📍 **{titulo}**\n🏢 Empresa: {empresa}\n🌎 Local: {local}\n\n🔗 **CANDIDATURA:**\n{link_direto}")
            vagas_enviadas += 1

    status = f"✅ {vagas_enviadas} enviadas" if vagas_enviadas > 0 else "ℹ️ Sem vagas novas"
    relatorio = (
        f"📊 **VARREDURA EXECUTADA**\n"
        f"⏰ {agora.strftime('%H:%M:%S')}\n"
        f"🔎 {cargo_da_vez} em {local_da_vez}\n"
        f"📝 Status: {status}"
    )
    bot.send_message(CHAT_ID, relatorio, parse_mode="Markdown")
    
    return "Busca Concluída!", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)