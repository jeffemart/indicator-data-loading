import mysql.connector
from mysql.connector import errorcode
import os
import logging
from session import conector
from dotenv import load_dotenv

# Configuração básica do logger
log_folder = "log"
os.makedirs(log_folder, exist_ok=True)
log_file = os.path.join(log_folder, "file.log")

logging.basicConfig(level=logging.DEBUG, filename=log_file, filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')

# ...
connection = conector.Connection()
con = connection.connect()
