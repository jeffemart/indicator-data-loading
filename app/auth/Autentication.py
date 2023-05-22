import requests
import logging
import json
import os
# ...
from dotenv import load_dotenv


class Login_in:
    def __init__(self, url=os.getenv("ROUTE_DESK_AUTH")):
        self.__token = ''
        self.url = url

    def Login(self) -> str:
        # <!--access credentials to authenticate
        load_dotenv()
        header = {'Authorization': os.getenv("AUTHORIZATION"),
                  'content-type': 'application/json'}
        params = json.dumps(
            {'PublicKey': os.getenv("PUBLIC_KEY")})

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