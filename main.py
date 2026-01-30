import os
import time
import requests
from telebot import TeleBot

# Configurações via Variáveis de Ambiente no Render
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = TeleBot(TOKEN)

# Lista de fontes para o relatório
FONTES = ["Indeed", "LinkedIn", "InfoJobs", "Google Jobs"]

def buscar_vagas_exemplo(fonte):
    """
    Simulação de busca. Substitua pela sua lógica de scrap real
    ou integração com APIs específicas de cada site.
    """
    # Aqui retornamos uma lista vazia apenas para demonstrar o relatório de '0 vagas'
    return []

def iniciar_monitoramento():
    # Mensagem de inicialização ajustada
    msg_inicio = "🤖 **Bot de Vagas ATIVO no Render!**\n\nMonitoramento iniciado com sucesso. Você receberá relatórios periódicos aqui."
    bot.send_message(CHAT_ID, msg_inicio, parse_mode="Markdown")
    
    while True:
        print("Iniciando ciclo de verificação...")
        relatorio = "📊 **Relatório de Pesquisa:**\n"
        relatorio += f"🕒 Hora: {time.strftime('%H:%M:%S')}\n\n"
        
        vagas_totais_ciclo = 0
        
        for fonte in FONTES:
            # Simula a busca em cada site
            vagas_encontradas = buscar_vagas_exemplo(fonte)
            quantidade = len(vagas_encontradas)
            
            # Adiciona ao relatório de texto
            relatorio += f"🔹 {fonte}: {quantidade} novas vagas\n"
            
            # Se houver vagas, envia uma por uma
            for vaga in vagas_encontradas:
                bot.send_message(CHAT_ID, f"📢 **Nova Vaga no {fonte}!**\n{vaga}")
                vagas_totais_ciclo += 1
        
        # Envia o relatório de status, mesmo que não encontre nada
        if vagas_totais_ciclo == 0:
            relatorio += "\nℹ️ Nenhuma vaga nova encontrada nos filtros."
        
        bot.send_message(CHAT_ID, relatorio, parse_mode="Markdown")
        
        # Espera 1 hora (3600 segundos) para a próxima verificação
        # No Render Free, o bot pode 'dormir', mas o loop tentará mantê-lo ativo
        print("Ciclo finalizado. Aguardando 1 hora...")
        time.sleep(3600)

if __name__ == "__main__":
    try:
        iniciar_monitoramento()
    except Exception as e:
        print(f"Erro crítico no sistema: {e}")