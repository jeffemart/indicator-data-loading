import os
import jwt
import logging
import mysql.connector
from dotenv import set_key, load_dotenv
from mysql.connector import errorcode

class database:
    def __init__(self, token):
        self.con = None
        self.token = token
        self.connected = False  # Controla se a conexão já foi estabelecida
        load_dotenv()

        # Acessa as variáveis de ambiente carregadas - Mysql
        self.mysql_host = os.getenv("MYSQL_HOST")
        self.mysql_user = os.getenv("MYSQL_ROOT_USER")
        self.mysql_password = os.getenv("MYSQL_ROOT_PASSWORD")
        self.mysql_database = os.getenv("MYSQL_DATABASE")

    def mysql(self):
        if not self.connected:  # Verifica se a conexão já foi estabelecida
            try:
                self.con = mysql.connector.connect(
                    host=self.mysql_host, user=self.mysql_user, password=self.mysql_password,
                    database=self.mysql_database)
                logging.info(self.con)
                self.connected = True  # Define o flag de conexão estabelecida

                if not self.token:  # Verifica se o token não está definido
                    # Gerar o token JWT
                    logging.info("Gerando token...")
                    encoded_token = jwt.encode({"MYSQL_HOST": self.mysql_host, "MYSQL_ROOT_USER": self.mysql_user, "MYSQL_ROOT_PASSWORD": self.mysql_password, "MYSQL_DATABASE": self.mysql_database, }, "chave_secreta", algorithm="HS256")
                    self.token = "Bearer " + encoded_token

                    # Salvar o token no arquivo .env
                    load_dotenv()
                    set_key('.env', 'APP_KEY', self.token)
                    logging.info("Token gerado e salvo.")

            except mysql.connector.Error as error:
                if error.errno == errorcode.ER_BAD_DB_ERROR:
                    logging.error("Database doesn't exist")
                elif error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    logging.error("User name or password is wrong")
                else:
                    logging.error(error)

        return self.con