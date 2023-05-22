from auth import Autentication
import requests
import logging
import json


class Data:
    def __init__(self, cod=['']):
        call_class = Autentication.login_in()
        call_class.login()
        self.__token = call_class.get_token()
        print(self.__token)
        
        self.url_data = 'https://api.desk.ms/Relatorios/imprimir'
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
            with open(f'../arquivos/{self.cod}.json', 'w', encoding='utf8') as log:
                json.dump(response.json(), log,
                            indent=4, ensure_ascii=False)
        else:
            logging.warning(
                f"Falha ao realizar o download do código {self.cod}")