import mysql.connector
import logging
import jwt
import os
from mysql.connector import errorcode
from dotenv import load_dotenv
from dotenv import set_key


class Connection:
    def __init__(self):
        self.con = None
        # Carrega as variáveis de ambiente do arquivo .env
        load_dotenv()

        # Acessa as variáveis de ambiente carregadas
        self.mysql_host = os.getenv("DB_HOST")
        self.mysql_user = os.getenv("MYSQL_USER")
        self.mysql_password = os.getenv("MYSQL_PASSWORD")
        self.mysql_database = os.getenv("MYSQL_DATABASE")

    def connect(self):
        try:
            self.con = mysql.connector.connect(
                host=self.mysql_host, user=self.mysql_user, password=self.mysql_password, database=self.mysql_database)
            logging.info(self.con)

            # Criação do token JWT
            payload = {"username": "example_user", "role": "admin"}  # Informações de acesso do usuário
            secret_key = "my_secret_key"  # Chave secreta para assinar o token
            token = jwt.encode(payload, secret_key, algorithm="HS256")

            logging.info("APP_KEY: " + token)

            # Salvar o token no arquivo .env
            load_dotenv()
            set_key('.env', 'APP_KEY', token)

        except mysql.connector.Error as error:
            if error.errno == errorcode.ER_BAD_DB_ERROR:
                logging.error("Database doesn't exist")
            elif error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                logging.error("User name or password is wrong")
            else:
                logging.error(error)

        return self.con