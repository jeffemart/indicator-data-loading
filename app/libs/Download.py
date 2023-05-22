import requests
import logging
import json
import os
# ...
from auth import Autentication
from dotenv import load_dotenv


class Data:
    def __init__(self, cod=['']):
        call_class = Autentication.Login_in()
        call_class.Login()
        self.__token = call_class.Get_token()
        print(self.__token)
        load_dotenv()
        
        self.url_data = os.getenv('ROUTE_DOWNLOAD')
        self.header = {'Authorization': f'{self.__token}'}
        self.cod = cod

    def Report(self):
        # <!--access credentials to authenticate
        params = json.dumps({'Chave': f'{self.cod}'})
        response = requests.post(
            self.url_data, headers=self.header, data=params)
        logging.debug(response)
        # <!--condition to check if response returned
        if response.status_code == 200:
            with open(f'./app/files/{self.cod}.json', 'w', encoding='utf8') as log:
                json.dump(response.json(), log,
                            indent=4, ensure_ascii=False)
        else:
            logging.warning(
                f"Falha ao realizar o download do código {self.cod}")