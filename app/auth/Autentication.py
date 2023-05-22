import requests
import logging
import json 
# ...
from dotenv import load_dotenv


class Login_in:
    def __init__(self, url='https://api.desk.ms/Login/autenticar'):
        self.__token = ''
        self.url = url

    def Login(self) -> str:
        # <!--access credentials to authenticate
        header = {'Authorization': 'fe0d0bda1e7ada6f755145a094ebdbfd50c3ab9c',
                  'content-type': 'application/json'}
        params = json.dumps(
            {'PublicKey': 'd8913f9062094f139a6f949f06f1afacf282a509'})

        # <!--request to authenticate
        response = requests.post(self.url, headers=header, data=params)
        logging.debug(response)
        
        # <!--condition to check if response returned
        if response.status_code == 200:
            self.__token = response.json()
        else:
            logging.warning("Falha na requisição do token")

    def Get_token(self):
        return self.__token