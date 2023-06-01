import os
import time
import datetime
import schedule
import logging
# ...
from libs import chamados
from libs import interacoes
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

# Agendar a execução do script a cada minuto
schedule.every(3).minutes.do(Routine)

# Manter o script em execução
while True:
    schedule.run_pending()
    time.sleep(1) 