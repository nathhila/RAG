import os
from abc import ABC, abstractmethod
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langsmith import traceable
from sqlalchemy import text as sql_text

from database import db
from embedding import embedding_m


load_dotenv()

MODEL = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="openai/gpt-oss-120b",
    temperature=0,
)
PROJECT_ROOT = Path(__file__).resolve().parent


def _build_prompt(docs, question: str) -> str:
    return f"""Você é um assistente de uma loja de móveis que ajuda funcionários com informações internas da empresa.

Seu papel é analisar os dados fornecidos abaixo e responder à pergunta do usuário de forma clara, amigável e objetiva.

Diretrizes:
- Use apenas as informações presentes nos dados fornecidos.
- Não invente informações ou faça suposições.
- Se não houver informação suficiente para responder, diga claramente que não sabe.
- Responda de forma natural, como se estivesse ajudando um colega de trabalho.
- Evite termos muito técnicos ou respostas robóticas.

Dados disponíveis:
{docs}

Pergunta do usuário:
{question}

Resposta:"""


def _save_answer(answer: str):
    with open(PROJECT_ROOT / "respostas.txt", "a", encoding="utf-8") as file:
        file.write(f"{answer}\n\n")


def _as_text(response) -> str:
    return getattr(response, "content", str(response))


class BuscaGeral(ABC):
    """Interface base para estratégias de busca por similaridade."""

    @abstractmethod
    def search_embedding(self, input_text: str) -> pd.DataFrame:
        raise NotImplementedError

    @abstractmethod
    def get_data(self, data_frame: pd.DataFrame, input_text: str):
        raise NotImplementedError

    @abstractmethod
    def post_response(self, data, input_text: str) -> str:
        raise NotImplementedError


class Departamento(BuscaGeral):

    @traceable
    def search_embedding(input_text: str):
        embedding = embedding_m.get_embeddings(input_text)

        script = sql_text(
            f"""
            SELECT id_departamento, cosine_distance(embedding, '{embedding}') AS cosine_dist
            FROM embedding_departamento
            WHERE embedding IS NOT NULL
            ORDER BY cosine_dist ASC
            LIMIT 5;
            """
        )
        registro = db.consult_db(script)

        if not registro:
            return pd.DataFrame(columns=["id_departamento", "cosine_dist"])

        data_frame = pd.DataFrame(registro, columns=["id_departamento", "cosine_dist"])
        Departamento.get_data(data_frame, input_text)
        return data_frame

    @traceable
    def get_data(data_frame, input_text: str):
        departamento_data = []

        for row in data_frame.itertuples(index=False):
            id_departamento = row[0]
            script = sql_text(
                f"""
                SELECT id_departamento, nome_departamento, sigla, num_funcionarios
                FROM departamento
                WHERE id_departamento = {id_departamento}
                """
            )
            registro = db.consult_db(script=script)

            if registro:
                data = pd.DataFrame(
                    registro,
                    columns=["id_departamento", "nome_departamento", "sigla", "num_funcionarios"],
                )
                departamento_data.append(data)

        Departamento.post_response(departamento_data, input_text)
        return departamento_data

    @traceable
    def post_response(departamento_data, input_text: str):
        if not departamento_data:
            answer = "Não encontrei informações suficientes para responder com base nos dados disponíveis."
            _save_answer(answer)
            return answer

        response = MODEL.invoke(_build_prompt(departamento_data, input_text))
        answer = _as_text(response)
        _save_answer(answer)
        return answer


class Funcionario(BuscaGeral):

    @traceable
    def search_embedding(input_text: str):
        embedding = embedding_m.get_embeddings(input_text)

        script = sql_text(
            f"""
            SELECT id_funcionario_ref, cosine_distance(embedding, '{embedding}') AS cosine_dist
            FROM embedding_funcionario
            WHERE embedding IS NOT NULL
            ORDER BY cosine_dist ASC
            LIMIT 5;
            """
        )
        registro = db.consult_db(script)

        if not registro:
            return pd.DataFrame(columns=["id_funcionario", "cosine_dist"])

        data_frame = pd.DataFrame(registro, columns=["id_funcionario", "cosine_dist"])
        Funcionario.get_data(data_frame, input_text)
        return data_frame

    @traceable
    def get_data(data_frame, input_text: str):
        funcionario_data = []

        for row in data_frame.itertuples(index=False):
            id_funcionario_ref = row[0]
            script = sql_text(
                f"""
                SELECT id_funcionario, nome, cpf, endereco, contato
                FROM funcionario
                WHERE id_funcionario = {id_funcionario_ref}
                """
            )
            registro = db.consult_db(script=script)

            if registro:
                data = pd.DataFrame(
                    registro,
                    columns=["id_funcionario", "nome", "cpf", "endereco", "contato"],
                )
                funcionario_data.append(data)

        Funcionario.post_response(funcionario_data, input_text)
        return funcionario_data

    @traceable
    def post_response(funcionario_data, input_text: str):
        if not funcionario_data:
            answer = "Não encontrei informações suficientes para responder com base nos dados disponíveis."
            _save_answer(answer)
            return answer

        response = MODEL.invoke(_build_prompt(funcionario_data, input_text))
        answer = _as_text(response)
        _save_answer(answer)
        print(answer)
        
        return answer


class Produto(BuscaGeral):

    @traceable
    def search_embedding(input_text: str):
        embedding = embedding_m.get_embeddings(input_text)

        if embedding is None:
            raise ValueError("O embedding não foi gerado corretamente.")

        embedding_str = "[" + ",".join(map(str, embedding)) + "]"
        script = sql_text(
            f"""
            SELECT id_produto_ref, cosine_distance(embedding, '{embedding_str}') AS cos_similarity
            FROM embedding_produto
            WHERE embedding IS NOT NULL
            ORDER BY cos_similarity ASC
            LIMIT 5
            """
        )
        registro = db.consult_db(script, {"embedding_str": embedding_str})

        if not registro:
            return pd.DataFrame(columns=["id_produto_ref", "cos_similarity"])

        data_frame = pd.DataFrame(registro, columns=["id_produto_ref", "cos_similarity"])
        Produto.get_data(data_frame, input_text)
        return data_frame

    @traceable
    def get_data(data_frame, input_text: str):
        data_produto = []

        for row in data_frame.itertuples(index=False):
            id_produto_ref = row[0]
            script = sql_text(
                f"""
                SELECT DISTINCT *
                FROM produto
                WHERE id_produto = {id_produto_ref}
                """
            )
            registro = db.consult_db(script)

            if registro:
                data = pd.DataFrame(
                    registro,
                    columns=["id_produto", "nome", "marca", "id_setor", "preco_unitario"],
                )
                data_produto.append(data)

        Produto.post_response(data_produto, input_text)
        return data_produto

    @traceable
    def post_response(data_produto, input_text: str):
        if not data_produto:
            answer = "Não encontrei informações suficientes para responder com base nos dados disponíveis."
            _save_answer(answer)
            return answer

        response = MODEL.invoke(_build_prompt(data_produto, input_text))
        answer = _as_text(response)
        _save_answer(answer)
        return answer

