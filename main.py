import time # Importante para o tempo de espera
from datetime import datetime

from config import CARGOS_PERMITIDOS
from ranking import ranquear_vagas, formatar_vaga
from telegram_bot import enviar_telegram

from fontes.infojobs import buscar_vagas_infojobs
from fontes.indeed import buscar_vagas_indeed
from fontes.gupy import buscar_vagas_gupy
from fontes.vagas import buscar_vagas_vagas
from fontes.burh import buscar_vagas_burh
from fontes.glassdoor import buscar_vagas_glassdoor
from fontes.linkedin import buscar_vagas_linkedin
from fontes.sine import buscar_vagas_sine
from fontes.mogiconecta import buscar_vagas_mogiconecta

def executar_automacao():
    print("\n🚀 MONITOR DE VAGAS INICIADO")
    print("🕒", datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    print("🔎 Buscando vagas...")
    print("🔑 Cargos permitidos:", ", ".join(CARGOS_PERMITIDOS))

    todas_as_vagas = []

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
            vagas = func()
            print(f"✅ {nome}: {len(vagas)} vagas")
            todas_as_vagas.extend(vagas)
        except Exception as e:
            print(f"❌ Erro em {nome}: {e}")

    vagas_rankeadas = ranquear_vagas(todas_as_vagas)

    if not vagas_rankeadas:
        print("ℹ️ Nenhuma vaga válida encontrada — canal NÃO será notificado.")
        return

    mensagem = "📊 *RANKING DE VAGAS A&B*\n\n"
    for vaga in vagas_rankeadas[:15]:
        mensagem += formatar_vaga(vaga) + "\n"

    enviar_telegram(mensagem)
    print("📢 Mensagem enviada ao Telegram com sucesso!")

if __name__ == "__main__":
    # LOOP INFINITO PARA RODAR 24/7
    while True:
        try:
            executar_automacao()
            
            # Define o tempo de espera (ex: 3600 segundos = 1 hora)
            intervalo = 3600 
            print(f"😴 Ciclo finalizado. Próxima busca em {intervalo/60:.0f} minutos...")
            time.sleep(intervalo)
            
        except Exception as erro_global:
            print(f"⚠️ Erro crítico no loop: {erro_global}")
            print("Tentando reiniciar em 5 minutos...")
            time.sleep(300)