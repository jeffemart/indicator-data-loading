import os
import json
import logging
import mysql.connector
# ...
from libs import download
from session import conector
from datetime import datetime


class callsolicitantes:
    def __init__(self) -> None:
        # <!--constructor to get token and report download
        info = download.data('139')
        info.report()
        
        with open('./files/139.json', 'r', encoding='utf_8') as desk:
                    self.relatorio = json.load(desk)

        # Carrega o token da variável de ambiente APP_KEY
        self.token = os.getenv("APP_KEY")

        # Cria uma instância da classe database
        self.db = conector.database(self.token)
    
    def solicitantes(self):
        # Função para inserir ou atualizar os dados no banco de dados
        con = self.db.mysql()
        cu = con.cursor()

        # Percorre os dados do JSON
        for item in self.relatorio['root']:
            # query para verificar se o usuário já existe
            query = "SELECT * FROM solicitantes WHERE ChaveUsuario = %s"
            cu.execute(query, (item.get('ChaveUsuario'),))
            result = cu.fetchone()

            # Verifica se o item já existe no banco de dados
            if result:
                print("Solicitante já existe!")
            else:
                # Insere um novo item
                query = "INSERT INTO solicitantes (ChaveUsuario, NomeUsuario, SobrenomeUsuario, Vip, SequenciaDepartamento, NomeDepartamento, SequenciaLocal, NomeLocal, SolicitanteEmail, EnderecoSolicitante, UfSolicitante, CepSolicitante) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                values = (
                    item.get('ChaveUsuario'),
                    item.get('NomeUsuario'),
                    item.get('SobrenomeUsuario'),
                    item.get('Vip'),
                    item.get('SequenciaDepartamento'),
                    item.get('NomeDepartamento'),
                    item.get('SequenciaLocal'),
                    item.get('NomeLocal'),
                    item.get('SolicitanteEmail'),
                    item.get('EnderecoSolicitante'),
                    item.get('UfSolicitante'),
                    item.get('CepSolicitante')
                )
                cu.execute(query, values)
                print("Solicitante inserido!")

        # Efetua o commit das alterações
        con.commit()

        # Fecha a conexão com o banco de dados
        cu.close()
        con.close()