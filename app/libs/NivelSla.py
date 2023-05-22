# ...
from session import conector
from datetime import datetime


# Função para inserir ou atualizar os dados no banco de dados
def insert_or_update_data(data):
    # Faz a conexão com o banco de dados
    # ...
    conection = conector.conection()
    con = conection.conect()
    cursor = con.cursor()

    # Percorre os dados do JSON
    for item in data['root']:
        # Formata a data de finalização (considerando '00-00-0000' como valor nulo)
        if item['DataCriacao'] == '00-00-0000':
            data_criacao_convertida = None
        else:
            data_criacao_convertida = datetime.strptime(
                item['DataCriacao'], '%d-%m-%Y').strftime('%Y-%m-%d')

        if item['DataFinalizacao'] == '00-00-0000':
            data_finalizacao_convertida = None
        else:
            data_finalizacao_convertida = datetime.strptime(
                item['DataFinalizacao'], '%d-%m-%Y').strftime('%Y-%m-%d')

        query = "SELECT * FROM chamados WHERE CodInterno = %s"
        cursor.execute(query, (item['CodInterno'],))
        result = cursor.fetchone()

        # Verifica se o item já existe no banco de dados
        if result:
            # Atualiza a linha existente
            query = "UPDATE chamados SET CodChamado = %s, DataCriacao = %s, DataFinalizacao = %s, ChaveAutoCategoria = %s, HoraFinalizacao = %s, FirstCall = %s, ChaveOperador = %s, ChaveUsuario = %s, ChaveSla = %s WHERE CodInterno = %s"
            cursor.execute(query, (
                item.get('CodChamado'),
                data_criacao_convertida,
                data_finalizacao_convertida,
                item.get('ChaveAutoCategoria'),
                item.get('HoraFinalizacao'),
                item.get('FirstCall'),
                item.get('ChaveOperador'),
                item.get('ChaveUsuario'),
                item.get('ChaveSla'),
                item.get('CodInterno')
            ))
            print("Registro atualizado!")

        else:
            # Insere um novo item
            query = "INSERT INTO chamados (CodInterno, CodChamado, DataCriacao, DataFinalizacao, ChaveAutoCategoria, HoraFinalizacao, FirstCall, ChaveOperador, ChaveUsuario, ChaveSla) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (
                item.get('CodInterno'),
                item.get('CodChamado'),
                data_criacao_convertida,
                data_finalizacao_convertida,
                item.get('ChaveAutoCategoria'),
                item.get('HoraFinalizacao'),
                item.get('FirstCall'),
                item.get('ChaveOperador'),
                item.get('ChaveUsuario'),
                item.get('ChaveSla')
            ))
            print("Registro inserido!")

    # Efetua o commit das alterações
    con.commit()

    # Fecha a conexão com o banco de dados
    cursor.close()
    con.close()


insert_or_update_data(data)
