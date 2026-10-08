import logging
import time

import pandas as pd
from sqlalchemy import text as sql_text

import db
from embedding.embedding_m import get_embeddings


def funcionario_emb(script):
    try:
        registro = db.consult_db(script=script)
        if registro is None:
            return None

        data_frame = pd.DataFrame(
            registro,
            columns=["id_funcionario", "id_departamento", "nome", "cpf", "endereco", "contato"],
        )

        for row in data_frame.itertuples(index=False):
            id_funcionario_ref = row[0]
            text = f"{row[1]} {row[2]} {row[3]} {row[4] or ''} {row[5]}"
            embedding = get_embeddings(text)
            script_sql = sql_text(
                """
                INSERT INTO embedding_funcionario (id_funcionario_ref, embedding)
                VALUES (:id_funcionario_ref, :embedding)
                """
            )
            db.exe_db(
                script=script_sql,
                params={"id_funcionario_ref": id_funcionario_ref, "embedding": embedding},
            )

        return 1
    except Exception as exc:
        logging.error("Erro ao executar %s. Detalhes: %s", script, exc)
        return None


def setor_emb(script):
    try:
        registro = db.consult_db(script=script)
        if registro is None:
            return None

        data_frame = pd.DataFrame(registro, columns=["id_setor", "nome"])
        for row in data_frame.itertuples(index=False):
            id_setor = row[0]
            text = f"{row[1]}"
            embedding = get_embeddings(text)

            script_sql = sql_text(
                """
                INSERT INTO embedding_setor (id_setor, embedding)
                VALUES (:id_setor, :embedding)
                """
            )
            db.exe_db(script=script_sql, params={"id_setor": id_setor, "embedding": embedding})
        return 1
    except Exception as exc:
        logging.error("Erro ao executar %s. Detalhes: %s", script, exc)
        return None


def departamento_emb(script):
    try:
        registro = db.consult_db(script=script)
        if registro is None:
            return None

        data_frame = pd.DataFrame(
            registro,
            columns=["id_departamento", "nome_departamento", "sigla", "num_funcionarios"],
        )
        for row in data_frame.itertuples(index=False):
            id_departamento = row[0]
            text = f"{row[1]} {row[2]} {row[3]}"
            embedding = get_embeddings(text)

            script_sql = sql_text(
                """
                INSERT INTO embedding_departamento (id_departamento, embedding)
                VALUES (:id_departamento, :embedding)
                """
            )
            db.exe_db(
                script=script_sql,
                params={"id_departamento": id_departamento, "embedding": embedding},
            )
        return 1
    except Exception as exc:
        logging.error("Erro ao executar %s. Detalhes: %s", script, exc)
        return None


def produto_emb(script):
    try:
        registro = db.consult_db(script=script)
        if registro is None:
            return None

        data_frame = pd.DataFrame(
            registro,
            columns=["id_produto", "nome", "marca", "id_setor", "preco_unitario"],
        )
        for row in data_frame.itertuples(index=False):
            id_produto_ref = row[0]
            text = f"{row[1]} {row[2]} {row[3]} {row[4]}"
            embedding = get_embeddings(text)

            script_sql = sql_text(
                """
                INSERT INTO embedding_produto (id_produto_ref, embedding)
                VALUES (:id_produto_ref, :embedding)
                """
            )
            db.exe_db(
                script=script_sql,
                params={"id_produto_ref": id_produto_ref, "embedding": embedding},
            )
        return 1
    except Exception as exc:
        logging.error("Erro ao executar %s. Detalhes: %s", script, exc)
        return None


if __name__ == "__main__":
    tempo_inicial = time.time()
    logging.basicConfig(filename="erros_banco.log", level=logging.ERROR)

    script_funcionario = sql_text(
        """
        SELECT id_funcionario, id_departamento, nome, cpf, endereco, contato
        FROM funcionario
        WHERE id_funcionario NOT IN
        (SELECT id_funcionario_ref FROM embedding_funcionario);
        """
    )
    funcionario_emb(script=script_funcionario)

    script_produto = sql_text(
        """
        SELECT id_produto, nome, marca, id_setor, preco_unitario
        FROM produto
        WHERE id_produto NOT IN
        (SELECT id_produto_ref FROM embedding_produto);
        """
    )
    produto_emb(script=script_produto)

    script_departamento = sql_text(
        """
        SELECT id_departamento, nome_departamento, sigla, num_funcionarios
        FROM departamento
        WHERE id_departamento NOT IN
        (SELECT id_departamento FROM embedding_departamento)
        """
    )
    departamento_emb(script=script_departamento)

    script_setor = sql_text(
        """
        SELECT id_setor, nome
        FROM setor
        WHERE id_setor NOT IN
        (SELECT id_setor FROM embedding_setor)
        """
    )
    setor_emb(script=script_setor)

    tempo_final = time.time()
    print(f"Tempo de processamento: {tempo_final - tempo_inicial} segundos")