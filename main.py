from enviar_telegram import enviar
from datetime import datetime
import time

def gerar_relatorio():
    hoje = datetime.now().strftime("%d/%m/%Y")

    mensagem = f"""
📊 <b>RELATÓRIO DIÁRIO DE VAGAS – A&B</b>
📅 {hoje}

1️⃣ <b>Maitre</b>
Empresa: Restaurante Premium XPTO  
Local: São Paulo – SP  
Salário: R$ 4.500 – R$ 6.000  
Contrato: CLT  

2️⃣ <b>Supervisor de Restaurante</b>
Empresa: Rede Gastronômica Alfa  
Local: Rio de Janeiro – RJ  
Salário: R$ 5.000  
Contrato: CLT  

3️⃣ <b>Supervisor de A&B</b>
Empresa: Hotel 4⭐  
Local: Curitiba – PR  
Salário: A combinar  
Contrato: CLT  

🔎 <i>Vagas filtradas: últimos 3 dias</i>
🏨 <i>Fontes: LinkedIn, Indeed, Glassdoor</i>
"""

    enviar(mensagem)

if __name__ == "__main__":
    print("🚀 MONITOR DE VAGAS INICIADO")

    while True:
        agora = datetime.now().strftime("%H:%M")

        if True:

            gerar_relatorio()
            time.sleep(60)  # evita enviar duplicado

        time.sleep(20)

