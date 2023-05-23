import os
import time
import datetime
import schedule
import logging
# ...
from libs import Chamados
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
        # Coloque o código que você deseja executar aqui
        print("Executando o script...")
    else:
        print("Fora do horário de execução.")

# Agendar a execução do script a cada minuto
schedule.every().day.at("09:00").do(Routine)

# Manter o script em execução
while True:
    schedule.run_pending()
    time.sleep(1)