import requests
import logging
import json
import os
# ...
from dotenv import load_dotenv


class login_in:
    def __init__(self):
        self.__token = ''
        self.url = os.getenv('ROUTE_DESK_AUTH')

    def login(self) -> str:
        # <!--access credentials to authenticate
        load_dotenv()
        header = {'Authorization': os.getenv('AUTHORIZATION'),
                  'content-type': 'application/json'}
        params = json.dumps(
            {'PublicKey': os.getenv('PUBLIC_KEY')})

        # <!--request to authenticate
        response = requests.post(self.url, headers=header, data=params)
        logging.debug(response)
        
        # <!--condition to check if response returned
        if response.status_code == 200:
            self.__token = response.json()
        else:
            logging.warning("Falha na requisição do token")

    def get_token(self):
        return self.__token