# adicionar multiprocessing para testes

from langchain_ollama import OllamaEmbeddings
import db
import pandas as pd
from sqlalchemy import text as sql_text
from embedding.embedding_m import get_embeddings
import time
import logging

def funcionario_emb(script):

    try:
        registro = db.consult_db(script=script)
        # registro o resultado do query em um dataframe
        data_frame = pd.DataFrame(registro, columns=['id_funcionario', 'id_departamento', 'nome', 'cpf', 'endereco', 'contato'])

        # pra cada linha dentro do data frame eu atributo o id_funcinario_ref a partir do id_funcionario e faço o embedding no restante das linhas
        for row in data_frame.itertuples(index=False):

            id_funcionario_ref = row[0]
            text = f"{row[1]} {row[2]} {row[3]} {row[4] or ''} {row[5]}"
            embedding = get_embeddings(text)
            SCRIPT_SQL = sql_text("""
                INSERT INTO embedding_funcionario (id_funcionario_ref, embedding)
                VALUES (:id_funcionario_ref, :embedding)
            """)
            db.exe_db(script=SCRIPT_SQL, params={
                "id_funcionario_ref": id_funcionario_ref,
                "embedding": embedding
            })

        return 1
    except Exception as e:
        print(f'erro: {e}')
        logging.error(f'erro ao executar {script}. erro {e}')
        return None

def setor_emb(script):

    try:
        registro = db.consult_db(script=script)
        data_frame = pd.DataFrame(registro, columns=['id_setor', 'nome'])
        for row in data_frame.itertuples(index=False):

            id_setor = row[0]
            text = f'{row[1]}'
            embedding = get_embeddings(text)

            SCRIPT_SQL = sql_text("""
                INSERT INTO embedding_setor (id_setor, embedding)
                VALUES (:id_setor, :embedding)
            """)
            db.exe_db(script=SCRIPT_SQL, params={
                "id_setor": id_setor,
                "embedding": embedding
            })
        return 1
    
    except Exception as e:

        print(f'erro: {e}')
        logging.error(f'erro ao executar {script}. erro {e}')
        return None


def departamento_emb(script):
    
    try:
        registro = db.consult_db(script=SCRIPT_SQL)
        data_frame = pd.DataFrame(registro, columns=['id_departamento', 'nome_departamento', 'sigla', 'num_funcionarios'])
        for row in data_frame.itertuples(index=False):

            id_departamento = row[0]
            text = f'{row[1]} {row[2]} {row[3]}'
            embedding = get_embeddings(text)

            SCRIPT_SQL = sql_text("""
                INSERT INTO embedding_departamento (id_departamento, embedding)
                VALUES (:id_departamento, :embedding)
            """)
            db.exe_db(script=SCRIPT_SQL, params={
                "id_departamento": id_departamento,
                "embedding": embedding
            })
        return 1
    
    except Exception as e:

        print(f'erro: {e}')
        logging.error(f'erro ao executar {script}. erro {e}')
        return None


def produto_emb(script):

    try:
        registro = db.consult_db(script=script)
        data_frame = pd.DataFrame(registro, columns=['id_produto', 'nome', 'marca', 'id_setor', 'preco_unitario'])
        for row in data_frame.itertuples(index=False):

            id_produto_ref = row[0]
            text = f'{row[1]} {row[2]} {row[3]} {row[4]}'
            embedding = get_embeddings(text)

            SCRIPT_SQL = sql_text("""
                INSERT INTO embedding_produto (id_produto_ref, embedding)
                VALUES (:id_produto_ref, :embedding)
            """)
            db.exe_db(script=SCRIPT_SQL, params={
                "id_produto_ref": id_produto_ref,
                "embedding": embedding
            })
        return 1
    except Exception as e:
        print(f'erro: {e}')
        logging.error(f'erro ao executar {script}. erro {e}')
        return None


if __name__ == '__main__':

    tempo_inicial = time.time()


    logging.basicConfig(filename='erros_banco.log', level=logging.ERROR)
    print('TABELA 1')
    SCRIPT_SQL = sql_text("""
        SELECT id_funcionario, id_departamento, nome, cpf, endereco, contato
        FROM funcionario
        WHERE id_funcionario NOT IN 
        (SELECT id_funcionario_ref FROM embedding_funcionario);
    """)
    funcionario_emb(script=SCRIPT_SQL)


    print('TABELA 2')
    SCRIPT_SQL = sql_text("""
        SELECT id_produto, nome, marca, id_setor, preco_unitario
        FROM produto
        WHERE id_produto NOT IN 
        (SELECT id_produto_ref FROM embedding_produto);
    """)

    produto_emb(script=SCRIPT_SQL)
 

    print('TABELA 3')
    SCRIPT_SQL = sql_text("""
        SELECT id_departamento, nome_departamento, sigla, num_funcionarios
        FROM departamento
        WHERE id_departamento NOT IN
        (SELECT id_departamento FROM embedding_departamento)
    """)
 
    departamento_emb(script=SCRIPT_SQL)
    
    print('TABELA 4')
    SCRIPT_SQL = sql_text("""
        SELECT id_setor, nome 
        FROM setor
        WHERE id_setor NOT IN
        (SELECT id_setor FROM embedding_setor)
    """)

    setor_emb(script=SCRIPT_SQL)

    tempo_final = time.time()

    print(f'tempo de processsamento: {tempo_final - tempo_inicial} segundos')