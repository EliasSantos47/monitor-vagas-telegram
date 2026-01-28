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
    """Função que realiza uma rodada completa de busca em todas as fontes"""
    print(f"\n--- 🕒 Início do Ciclo: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} ---")
    print(f"🔑 Filtrando por: {', '.join(CARGOS_PERMITIDOS)}")
    
    todas_as_vagas = []

    # Lista de fontes configuradas
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
            print(f"🔎 Buscando em {nome}...")
            vagas = func()
            print(f"✅ {nome}: {len(vagas)} vagas encontradas.")
            todas_as_vagas.extend(vagas)
        except Exception as e:
            # Se uma fonte falhar, o bot continua para a próxima em vez de travar
            print(f"❌ Erro ao buscar em {nome}: {e}")

    # Processamento e Ranking
    vagas_rankeadas = ranquear_vagas(todas_as_vagas)

    if not vagas_rankeadas:
        print("ℹ️ Nenhuma vaga compatível encontrada neste ciclo.")
        return

    # Formatação da mensagem para o Telegram
    mensagem = "📊 *RANKING DE VAGAS ATUALIZADO*\n\n"
    for vaga in vagas_rankeadas[:15]:
        mensagem += formatar_vaga(vaga) + "\n"

    # Envio para o canal configurado no Railway
    try:
        enviar_telegram(mensagem)
        print("📢 Notificação enviada ao Telegram!")
    except Exception as e:
        print(f"❌ Falha ao enviar mensagem para o Telegram: {e}")

if __name__ == "__main__":
    print("🚀 Automação configurada para rodar 24/7 na nuvem.")
    
    while True:
        try:
            executar_ciclo_de_busca()
            
            # Intervalo de 1 hora (3600 segundos) conforme solicitado
            INTERVALO_HORA = 3600 
            print(f"\n😴 Ciclo finalizado com sucesso.")
            print(f"Aguardando 60 minutos para a próxima verificação...")
            time.sleep(INTERVALO_HORA)
            
        except KeyboardInterrupt:
            print("\n🛑 Automação interrompida manualmente.")
            break
        except Exception as erro_critico:
            # Caso ocorra um erro inesperado, espera 5 minutos e reinicia o loop
            print(f"⚠️ ERRO CRÍTICO NO SISTEMA: {erro_critico}")
            print("Reiniciando em 300 segundos para evitar travamento...")
            time.sleep(300)