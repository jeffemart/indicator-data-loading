import os
import jwt
import logging
# import psycopg2
import mysql.connector
# ...
from dotenv import set_key
from dotenv import load_dotenv
from mysql.connector import errorcode


class database:
    def __init__(self):
        self.con = None
        # Carrega as variáveis de ambiente do arquivo .env
        load_dotenv()

        # Acessa as variáveis de ambiente carregadas - Mysql
        self.mysql_host = os.getenv("MYSQL_HOST")
        self.mysql_user = os.getenv("MYSQL_USER")
        self.mysql_password = os.getenv("MYSQL_PASSWORD")
        self.mysql_database = os.getenv("MYSQL_DATABASE")

        # Acessa as variáveis de ambiente carregadas - Postgrees
        self.postgrees_host = os.getenv("POSTGRES_HOST")
        self.postgrees_user = os.getenv("POSTGRES_USER")
        self.postgrees_password = os.getenv("POSTGRES_PASSWORD")
        self.postgrees_database = os.getenv("POSTGRES_DB")
        self.postgrees_port = os.getenv("POSTGRES_PORT")

    def mysql(self):
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
    
    # def postgrees(self):
    #     try:
    #         self.con = psycopg2.connect(
    #             dbname=self.postgrees_database, user=self.postgrees_user, password=self.postgrees_password, host=self.postgrees_host, port=self.postgrees_port)
    #         logging.info(self.con)

    #         # Criação do token JWT
    #         payload = {"username": "example_user", "role": "admin"}  # Informações de acesso do usuário
    #         secret_key = "my_secret_key"  # Chave secreta para assinar o token
    #         token = jwt.encode(payload, secret_key, algorithm="HS256")

    #         logging.info("APP_KEY: " + token)

    #         # Salvar o token no arquivo .env
    #         load_dotenv()
    #         set_key('.env', 'APP_KEY', token)

    #     except psycopg2.Error as error:
    #         if error.pgcode == '3D000':
    #             logging.error("Database doesn't exist")
    #         elif error.pgcode == '28P01':
    #             logging.error("User name or password is wrong")
    #         else:
    #             logging.error(error)

    #     return self.con
