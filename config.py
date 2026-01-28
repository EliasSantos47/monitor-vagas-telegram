import os

# ================================
# 🔐 TELEGRAM (Prioridade: Nuvem / Backup: Local)
# ================================
# Busca as variáveis do Railway. Se não existirem, usa os valores padrão abaixo.
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "8293582725:AAFp6tviJ5rVd7fVvoP7kun1b7uORX_hyIk")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT", "-1003555882210")

# ================================
# FILTROS DE CARGOS (BLOQUEIO TOTAL)
# ================================
CARGOS_PERMITIDOS = [
    "gerente a&b",
    "gerente de alimentos e bebidas",
    "gerente de bar",
    "assistente de a&b",
    "assistente de alimentos e bebidas",
    "supervisor a&b",
    "supervisor de alimentos e bebidas",
    "supervisor de bar",
    "chefe de bar",
    "maitre",
    "maitre executivo",
    "chefe de fila em bar"
]

# ================================
# PRIORIDADE / SCORE
# ================================
SCORE_CARGOS = {
    "gerente a&b": 100,
    "gerente de alimentos e bebidas": 100,
    "gerente de bar": 95,
    "maitre executivo": 90,
    "maitre": 85,
    "supervisor a&b": 80,
    "supervisor de alimentos e bebidas": 80,
    "supervisor de bar": 75,
    "chefe de bar": 70,
    "chefe de fila em bar": 65,
    "assistente de a&b": 60,
    "assistente de alimentos e bebidas": 60
}

# ================================
# FONTES ATIVAS (True = ativa | False = ignorada)
# ================================
FONTES_ATIVAS = {
    "infojobs": True,
    "indeed": True,
    "gupy": True,
    "vagas": True,
    "burh": True,
    "glassdoor": True,
    "linkedin": True,
    "sine": True,
    "mogiconecta": True
}

# ================================
# CONFIGURAÇÕES DE OPERAÇÃO
# ================================
ARQUIVO_HISTORICO = "historico.json"
MAX_VAGAS_POR_ENVIO = 10
INTERVALO_EXECUCAO_MINUTOS = 60  # Definido conforme sua solicitação