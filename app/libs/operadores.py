import json
import logging
import mysql.connector
# ...
from libs import download
from session import conector
from datetime import datetime


class calloperadores:
    def __init__(self) -> None:
        # <!--constructor to get token and report download
        info = download.data('144')
        info.report()
        
        with open('./files/144.json', 'r', encoding='utf_8') as desk:
                    self.relatorio = json.load(desk)
    
    def operadores(self):
        # Função para inserir ou atualizar os dados no banco de dados
        # ...
        conc = conector.database()
        con = conc.mysql()
        cu = con.cursor()

        # Percorre os dados do JSON
        for item in self.relatorio['root']:
            # query para verificar se o operador já existe
            query = "SELECT * FROM operadores WHERE ChaveOperador = %s"
            cu.execute(query, (item.get('ChaveOperador'),))
            result = cu.fetchone()

            # Verifica se o item já existe no banco de dados
            if result:
                print("Operador já existe!")
            else:
                # Insere um novo item
                query = "INSERT INTO operadores (ChaveOperador, NomeOperador, NomeCompletoOperador) VALUES (%s, %s, %s)"
                values = (
                    item.get('ChaveOperador'),
                    item.get('NomeOperador'),
                    item.get('NomeCompletoOperador')
                )
                cu.execute(query, values)
                print("Operador inserido!")

        # Efetua o commit das alterações
        con.commit()

        # Fecha a conexão com o banco de dados
        cu.close()
        con.close()