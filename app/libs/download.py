import requests
import logging
import json
import os
from auth import autentication
from dotenv import load_dotenv


class data:
    def __init__(self, cod=['']):
        load_dotenv()  # Carrega as variáveis de ambiente do arquivo .env
        self.url_data = os.getenv('ROUTE_DOWNLOAD')
        self.__token = os.getenv('APP_TOKEN')

        if not self.__token:  # Verifica se o token está vazio
            call_class = autentication.login_in()
            call_class.login()
            self.__token = call_class.get_token()
            print(self.__token)

        self.header = {'Authorization': f'{self.__token}'}
        self.cod = cod

    def report(self):
        # <!--access credentials to authenticate
        params = json.dumps({'Chave': f'{self.cod}'})
        response = requests.post(
            self.url_data, headers=self.header, data=params)
        logging.debug(response)
        # <!--condition to check if response returned
        if response.status_code == 200:
            with open(f'./files/{self.cod}.json', 'w', encoding='utf8') as desk:
                json.dump(response.json(), desk,
                            indent=4, ensure_ascii=False)
        else:
            logging.warning(
                f"Falha ao realizar o download do código {self.cod}")
