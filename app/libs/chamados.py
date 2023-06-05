import os
import json
import mysql.connector
# ...
from libs import download
from session import conector
from datetime import datetime, timedelta


class callchamados:
    def __init__(self) -> None:
        # <!--constructor to get token and report download
        # info = download.data('140')
        # info.report()
        
        with open('./files/140.json', 'r', encoding='utf_8') as desk:
                    self.relatorio = json.load(desk)

        # Carrega o token da variável de ambiente APP_KEY
        self.token = os.getenv("APP_KEY")

        # Cria uma instância da classe database
        self.db = conector.database(self.token)
    
    def priority(self):
        con = self.db.mysql()
        cu = con.cursor()

        for item in self.relatorio['root']:
            data_criacao_convertida = None
            data_finalizacao_convertida = None
            total_horas_abertura_finalizacao_convertido = None

            if item['DataCriacao'] != '00-00-0000':
                data_criacao_convertida = datetime.strptime(
                    item['DataCriacao'], '%d-%m-%Y').strftime('%Y-%m-%d')

            if item['DataFinalizacao'] != '00-00-0000':
                data_finalizacao_convertida = datetime.strptime(
                    item['DataFinalizacao'], '%d-%m-%Y').strftime('%Y-%m-%d')

            if item['TotalHorasAberturaFinalizacao']:
                duracao_parts = item['TotalHorasAberturaFinalizacao'].split(':')
                horas = int(duracao_parts[0])
                minutos = int(duracao_parts[1])
                segundos = int(duracao_parts[2])

                total_segundos = (horas * 3600) + (minutos * 60) + segundos

                total_horas_abertura_finalizacao_convertido = total_segundos

            query = "SELECT * FROM chamados WHERE CodInterno = %s"
            cu.execute(query, (item['CodInterno'],))
            result = cu.fetchone()

            if result:
                should_update = (
                    result[1] != item.get('CodChamado') or
                    result[2] != data_criacao_convertida or
                    result[3] != data_finalizacao_convertida or
                    result[4] != item.get('ChaveAutoCategoria') or
                    result[5] != item.get('HoraFinalizacao') or
                    result[6] != total_horas_abertura_finalizacao_convertido or
                    result[7] != item.get('FirstCall') or
                    result[8] != item.get('ChaveOperador') or
                    result[9] != item.get('ChaveUsuario') or
                    result[10] != item.get('ChaveSla')
                )

                if should_update:
                    query = """
                        UPDATE chamados SET
                        CodChamado = %s,
                        DataCriacao = %s,
                        DataFinalizacao = %s,
                        ChaveAutoCategoria = %s,
                        HoraFinalizacao = %s,
                        TotalHorasAberturaFinalizacao = %s,
                        FirstCall = %s,
                        ChaveOperador = %s,
                        ChaveUsuario = %s,
                        ChaveSla = %s
                        WHERE CodInterno = %s
                    """
                    cu.execute(query, (
                        item.get('CodChamado'),
                        data_criacao_convertida,
                        data_finalizacao_convertida,
                        item.get('ChaveAutoCategoria'),
                        item.get('HoraFinalizacao'),
                        total_horas_abertura_finalizacao_convertido,
                        item.get('FirstCall'),
                        item.get('ChaveOperador'),
                        item.get('ChaveUsuario'),
                        item.get('ChaveSla'),
                        item.get('CodInterno')
                    ))
                    print("Chamado atualizado!")
                else:
                    print("Chamado não precisa ser atualizado.")
            else:
                query = """
                    INSERT INTO chamados (
                        CodInterno,
                        CodChamado,
                        DataCriacao,
                        DataFinalizacao,
                        ChaveAutoCategoria,
                        HoraFinalizacao,
                        TotalHorasAberturaFinalizacao,
                        FirstCall,
                        ChaveOperador,
                        ChaveUsuario,
                        ChaveSla
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    )
                """
                cu.execute(query, (
                    item.get('CodInterno'),
                    item.get('CodChamado'),
                    data_criacao_convertida,
                    data_finalizacao_convertida,
                    item.get('ChaveAutoCategoria'),
                    item.get('HoraFinalizacao'),
                    total_horas_abertura_finalizacao_convertido,
                    item.get('FirstCall'),
                    item.get('ChaveOperador'),
                    item.get('ChaveUsuario'),
                    item.get('ChaveSla')
                ))
                print("Chamado inserido!")

            con.commit()

        cu.close()
        con.close()
 