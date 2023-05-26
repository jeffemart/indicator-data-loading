import os
import time
import datetime
import schedule
import logging
# ...
from libs import chamados
from libs import interacoes
from session import conector
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
    hora_atual = datetime.datetime.now().time()
    hora_inicio = datetime.time(9, 0, 0)
    hora_fim = datetime.time(17, 0, 0)

    if hora_inicio <= hora_atual <= hora_fim:
        print("testando")
        # # Poppulando dados na tabela de chamados
        # tabela_chamados = chamados.callchamados()
        # tabela_chamados.priority()

        # # Poppulando dados na tabela de interações
        # tabela_interacoes = interacoes.callinteracoes()
        # tabela_interacoes.interacoes()
    else:
        print("Fora do horário de execução.")

# Agendar a execução do script a cada minuto
schedule.every(15).minutes.do(Routine)

# Manter o script em execução
while True:
    schedule.run_pending()
    time.sleep(1) 