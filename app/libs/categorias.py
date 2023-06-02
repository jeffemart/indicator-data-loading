import json
import logging
import mysql.connector
# ...
from libs import download
from session import conector
from datetime import datetime


class callcategorias:
    def __init__(self) -> None:
        # <!--constructor to get token and report download
        info = download.data('143')
        info.report()
        
        with open('./files/143.json', 'r', encoding='utf_8') as desk:
                    self.relatorio = json.load(desk)
    
    def categorias(self):
        # Função para inserir ou atualizar os dados no banco de dados
        # ...
        conc = conector.database()
        con = conc.mysql()
        cu = con.cursor()

        # Percorre os dados do JSON
        for item in self.relatorio['root']:
            # query para verificar se a categoria já existe
            query = "SELECT * FROM categorias WHERE SequenciaCategoria = %s"
            cu.execute(query, (item.get('SequenciaCategoria'),))
            result = cu.fetchone()

            # Verifica se o item já existe no banco de dados
            if result:
                print("Categoria já existe!")
            else:
                # Insere um novo item
                query = "INSERT INTO categorias (GrupoAutoCategoriaSequencia, GrupoAutoCategoriaNome, SequenciaSubCategoria, NomeSubCategoria, SequenciaCategoria, NomeCategoria) VALUES (%s, %s, %s, %s, %s, %s)"
                values = (
                    item.get('GrupoAutoCategoriaSequencia'),
                    item.get('GrupoAutoCategoriaNome'),
                    item.get('SequenciaSubCategoria'),
                    item.get('NomeSubCategoria'),
                    item.get('SequenciaCategoria'),
                    item.get('NomeCategoria')
                )
                cu.execute(query, values)
                print("Registro inserido!")

        # Efetua o commit das alterações
        con.commit()

        # Fecha a conexão com o banco de dados
        cu.close()
        con.close()