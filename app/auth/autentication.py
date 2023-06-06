import requests
import logging
import json
import os
from dotenv import load_dotenv, set_key

class login_in:
    def __init__(self):
        self.__token = ''
        self.url = os.getenv('ROUTE_DESK_AUTH')
        load_dotenv()  # Carrega as variáveis de ambiente do arquivo .env

    def login(self) -> str:
        header = {
            'Authorization': os.getenv('AUTHORIZATION'),
            'content-type': 'application/json'
        }
        params = json.dumps({'PublicKey': os.getenv('PUBLIC_KEY')})

        response = requests.post(self.url, headers=header, data=params)
        logging.debug(response)

        if response.status_code == 200:
            self.__token = response.json()

            # Salvar o token na variável APP_TOKEN do arquivo .env
            load_dotenv()
            set_key('.env', 'APP_TOKEN', self.__token)
            logging.info("Token salvo no arquivo .env")
        else:
            logging.warning("Falha na requisição do token")

    def get_token(self):
        return self.__token
