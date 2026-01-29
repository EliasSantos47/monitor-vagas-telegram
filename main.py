import time
from datetime import datetime

# Importações de configuração e utilitários
from config import CARGOS_PERMITIDOS
from ranking import ranquear_vagas, formatar_vaga
from telegram_bot import enviar_telegram

# Importações das fontes de busca
from fontes.infojobs import buscar_vagas_infojobs
from fontes.indeed import buscar_vagas_indeed
from fontes.gupy import buscar_vagas_gupy
from fontes.vagas import buscar_vagas_vagas
from fontes.burh import buscar_vagas_burh
from fontes.glassdoor import buscar_vagas_glassdoor
from fontes.linkedin import buscar_vagas_linkedin
from fontes.sine import buscar_vagas_sine
from fontes.mogiconecta import buscar_vagas_mogiconecta

def executar_ciclo_de_busca():
    """Realiza a busca, gera relatório de status e envia vagas encontradas"""
    agora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    print(f"\n--- 🕒 Início do Ciclo: {agora} ---")
    
    todas_as_vagas = []
    relatorio_fontes = [] # Armazena o resultado de cada site para o relatório

    # Lista de fontes para iteração
    fontes = [
        ("InfoJobs", buscar_vagas_infojobs),
        ("Indeed", buscar_vagas_indeed),
        ("Gupy", buscar_vagas_gupy),
        ("Vagas.com", buscar_vagas_vagas),
        ("Burh", buscar_vagas_burh),
        ("Glassdoor", buscar_vagas_glassdoor),
        ("LinkedIn", buscar_vagas_linkedin),
        ("SINE", buscar_vagas_sine),
        ("Mogi Conecta", buscar_vagas_mogiconecta),
    ]

    for nome, func in fontes:
        try:
            print(f"🔎 Consultando {nome}...")
            vagas = func()
            qtd = len(vagas)
            todas_as_vagas.extend(vagas)
            relatorio_fontes.append(f"🔹 {nome}: {qtd} vagas")
        except Exception as e:
            print(f"❌ Erro em {nome}: {e}")
            relatorio_fontes.append(f"❌ {nome}: Falha na conexão")

    # Processamento e Filtro A&B
    vagas_rankeadas = ranquear_vagas(todas_as_vagas)
    qtd_filtradas = len(vagas_rankeadas)

    # --- MONTAGEM DA MENSAGEM DE STATUS (CHECKPOINT) ---
    status_msg = (
        f"🛰️ **RELATÓRIO DE MONITORAMENTO**\n"
        f"⏰ Horário: {agora}\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        + "\n".join(relatorio_fontes) + "\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"🎯 Vagas qualificadas (A&B): **{qtd_filtradas}**"
    )

    # Envia o status para você saber que o bot está ativo
    enviar_telegram(status_msg)

    # Se houver vagas qualificadas, envia o ranking em uma mensagem separada
    if qtd_filtradas > 0:
        print(f"📢 Enviando {qtd_filtradas} vagas para o Telegram...")
        mensagem_vagas = "📊 *RANKING DE VAGAS QUALIFICADAS*\n\n"
        for vaga in vagas_rankeadas[:15]:
            mensagem_vagas += formatar_vaga(vaga) + "\n"
        enviar_telegram(mensagem_vagas)
    else:
        print("ℹ️ Ciclo finalizado sem vagas qualificadas para os critérios de A&B.")

if __name__ == "__main__":
    print("🚀 Bot de Monitoramento iniciado em modo 24/7.")
    
    while True:
        try:
            executar_ciclo_de_busca()
            
            # Intervalo de 1 hora (3600 segundos)
            INTERVALO = 3600 
            print(f"😴 Dormindo por 60 minutos... Próxima busca em: {datetime.now().hour + 1}:00")
            time.sleep(INTERVALO)
            
        except Exception as erro_critico:
            print(f"🚨 ERRO CRÍTICO NO LOOP: {erro_critico}")
            # Em caso de erro grave, espera 5 minutos e reinicia

            time.sleep(300)
