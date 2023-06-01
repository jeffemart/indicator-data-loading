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
    
    def interacoes(self):
        # Função para inserir ou atualizar os dados no banco de dados
        # ...
        conc = conector.database()
        con = conc.mysql()
        cu = con.cursor()

        # Percorre os dados do JSON
        for item in self.relatorio['root']:
            # query para verificar se a interação já existe
            query = "SELECT * FROM interacoes WHERE CodInterno = %s and HoraAcaoInicio = %s"
            cu.execute(query, (item['CodInterno'], item['HoraAcaoInicio']))
            result = cu.fetchone()
            logging.info(result)
            
            # # Verifica se o item já existe no banco de dados
            if result:
                print("Interação já existe!")

            else:
                # Insere um novo item
                query = "INSERT INTO interacoes (CodInterno, DescricaoChamado, DataCriacaoAcao, HoraAcaoInicio, Protocolo, SequenciaStatus, StatusAcaoNomeRelatorio) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                cu.execute(query, (
                    item.get('CodInterno'),
                    item.get('DescricaoChamado'),
                    item.get('DataCriacaoAcao'),
                    item.get('HoraAcaoInicio'),
                    item.get('Protocolo'),
                    item.get('SequenciaStatus'),
                    item.get('StatusAcaoNomeRelatorio')
                ))
                print("Registro inserido!")

        # Efetua o commit das alterações
        con.commit()

        # Fecha a conexão com o banco de dados
        cu.close()
        con.close()