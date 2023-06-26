import os
import time
import datetime
import schedule
import logging
# ...
from libs import chamados
from libs import interacoes
from libs import categorias
from libs import operadores
from libs import solicitantes
from libs import sla
from session import conector
from datetime import datetime
from dotenv import load_dotenv

# Configuração básica do logger
load_dotenv()
log_folder = "log"
os.makedirs(log_folder, exist_ok=True)
log_file = os.path.join(log_folder, "file.log")

logging.basicConfig(level=logging.DEBUG, filename=log_file, filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')

# ...
def Routine():
    # Poppulando dados na tabela de chamados
    tabela_chamados = chamados.callchamados()
    tabela_chamados.priority()

    # Poppulando dados na tabela de interações
    tabela_interacoes = interacoes.callinteracoes()
    tabela_interacoes.interacoes()

    # Poppulando dados na tabela de operadores
    tabela_operadores = operadores.calloperadores()
    tabela_operadores.operadores()

    # Poppulando dados na tabela de categorias
    tabela_categorias = categorias.callcategorias()
    tabela_categorias.categorias()

    # Poppulando dados na tabela de solicitantes
    tabela_solicitantes = solicitantes.callsolicitantes()
    tabela_solicitantes.solicitantes()

    # Poppulando dados na tabela de sla
    tabela_sla = sla.callsla()
    tabela_sla.sla()

# Agendar a execução do script uma vez por dia às 11 horas da manhã
schedule.every().day.at("12:00").do(Routine)

# Manter o script em execução
while True:
    schedule.run_pending()
    time.sleep(1) 