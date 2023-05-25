import json
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
            # Formata a data de Acao (considerando '00-00-0000' como valor nulo)
            if item['DataCriacaoAcao'] == '00-00-0000':
                data_criacao_convertida = None
            else:
                data_criacao_convertida = datetime.strptime(
                    item['DataCriacaoAcao'], '%d-%m-%Y').strftime('%Y-%m-%d')

            query = "SELECT * FROM chamados WHERE CodInterno = %s"
            cu.execute(query, (item['CodInterno'],))
            result = cu.fetchone()

            # Verifica se o item já existe no banco de dados
            if result:
                # Atualiza a linha existente
                query = "UPDATE chamados SET CodChamado = %s, DataCriacao = %s, DataFinalizacao = %s, ChaveAutoCategoria = %s, HoraFinalizacao = %s, FirstCall = %s, ChaveOperador = %s, ChaveUsuario = %s, ChaveSla = %s WHERE CodInterno = %s"
                cu.execute(query, (
                    item.get('CodChamado'),
                    item.get('DescricaoChamado'),
                    data_criacao_convertida,
                    item.get('HoraAcaoInicio'),
                    item.get('Protocolo'),
                    item.get('SequenciaStatus'),
                    item.get('StatusAcaoNomeRelatorio')
                ))
                print("Registro atualizado!")

            else:
                # Insere um novo item
                query = "INSERT INTO chamados (CodInterno, CodChamado, DataCriacao, DataFinalizacao, ChaveAutoCategoria, HoraFinalizacao, FirstCall, ChaveOperador, ChaveUsuario, ChaveSla) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cu.execute(query, (
                    item.get('CodInterno'),
                    item.get('DescricaoChamado'),
                    data_criacao_convertida,
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
