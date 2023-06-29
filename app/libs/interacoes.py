import os
import json
import logging
import mysql.connector
# ...
from libs import download
from session import conector
from datetime import datetime


class callinteracoes:
    def __init__(self) -> None:
        # <!--constructor to get token and report download
        info = download.data('141')
        info.report()
        
        with open('./files/141.json', 'r', encoding='utf_8') as desk:
                    self.relatorio = json.load(desk)

        # Carrega o token da variável de ambiente APP_KEY
        self.token = os.getenv("APP_KEY")

        # Cria uma instância da classe database
        self.db = conector.database(self.token)

    def interacoes(self):
        # Função para inserir ou atualizar os dados no banco de dados
        con = self.db.postgres()
        cu = con.cursor()

        # Percorre os dados do JSON
        for item in self.relatorio['root']:
            # query para verificar se a interação já existe
            query = "SELECT * FROM deskmanager.interacoes WHERE CodInterno = %s and HoraAcaoInicio = %s"
            cu.execute(query, (item.get('CodInterno'), item.get('HoraAcaoInicio')))
            result = cu.fetchone()
            
            # Verifica se o item já existe no banco de dados
            if result:
                print("Interação já existe!")
            else:
                # Insere um novo item
                query = "INSERT INTO deskmanager.interacoes (CodInterno, NChamado, OperadorAcaoNomeCRelatorio, FantasiaClienteChamado, DataCriacaoAcao, HoraAcaoInicio, HoraAcaoFim, TotalHoras, NomeFormaAtendimento, DescricaoChamado, AssuntoChamado, Descricao) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cu.execute(query, (
                    item.get('CodInterno'),
                    item.get('NChamado'),
                    item.get('OperadorAcaoNomeCRelatorio'),
                    item.get('FantasiaClienteChamado'),
                    item.get('DataCriacaoAcao'),
                    item.get('HoraAcaoInicio'),
                    item.get('HoraAcaoFim'),
                    item.get('TotalHoras'),
                    item.get('NomeFormaAtendimento'),
                    item.get('DescricaoChamado'),
                    item.get('AssuntoChamado'),
                    item.get('Descricao')
                ))
                print("Interação inserida!")

        # Efetua o commit das alterações
        con.commit()

        # Fecha a conexão com o banco de dados
        cu.close()
        con.close()