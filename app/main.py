import os
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
# connection = conector.Connection()
# con = connection.connect()


chamados = Chamados.Calls()
chamados.Priority()