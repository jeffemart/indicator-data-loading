import json
import logging
import mysql.connector
# ...
from libs import download
from session import conector
from datetime import datetime


class callsla:
    def __init__(self) -> None:
        # <!--constructor to get token and report download
        info = download.data('142')
        info.report()
        
        with open('./files/142.json', 'r', encoding='utf_8') as desk:
            self.relatorio = json.load(desk)
    
    def sla(self):
        # Função para inserir ou atualizar os dados no banco de dados
        # ...
        conc = conector.database()
        con = conc.mysql()
        cu = con.cursor()

        # Percorre os dados do JSON
        for item in self.relatorio['root']:
            # query para verificar se a interação já existe
            query = "SELECT * FROM sla WHERE ChaveSla = %s"
            cu.execute(query, (item.get('ChaveSla'), ))
            result = cu.fetchone()
            
            # Verifica se o item já existe no banco de dados
            if result:
                print("SLA já existe!")
            else:
                # Insere um novo item
                query = "INSERT INTO sla (ChaveSla, NomeSla, SlaInterno, SlaContratual, TotalHorasAberturaFinalizacao, TotalHorasAberturaSegundoAtendimento, ChaveSlaStatusAtual, NomeSlaStatusAtual, NomeSla2Status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                values = (
                    item.get('ChaveSla'),
                    item.get('NomeSla'),
                    item.get('SlaInterno'),
                    item.get('SlaContratual'),
                    item.get('TotalHorasAberturaFinalizacao'),
                    item.get('TotalHorasAberturaSegundoAtendimento'),
                    item.get('ChaveSlaStatusAtual'),
                    item.get('NomeSlaStatusAtual'),
                    item.get('NomeSla2Status')
                )
                cu.execute(query, values)
                print("SLA inserido!")

        # Efetua o commit das alterações
        con.commit()

        # Fecha a conexão com o banco de dados
        cu.close()
        con.close()
