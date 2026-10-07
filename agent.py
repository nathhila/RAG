# strategy pattern pra implementar no agent.py
# adicionar parametros no código para deixar mais seguro
from abc import ABC, abstractmethod
from sqlalchemy import text as sql_text
# import queries_consult
from database import db
from embedding import embedding_m
from langchain_groq import ChatGroq
from langsmith import traceable

import os
import pandas as pd

from dotenv import load_dotenv


load_dotenv()
model = ChatGroq(api_key=os.getenv('GROQ_API_KEY'),
                 model='openai/gpt-oss-120b',
                 temperature=0)

# 1. Interface base usando ABC (Abstract Base Class)
class BuscaGeral(ABC):
    """Interface base para estratégias de busca"""
    
    @abstractmethod
    def search_embedding(self, input_text: str) -> pd.DataFrame:
        """Busca por embedding e retorna DataFrame com IDs e distâncias"""
        pass
    
    @abstractmethod
    def get_data(self, data_frame: pd.DataFrame, input_text: str) -> list:
        """Pega os dados completos baseado no DataFrame de embeddings"""
        pass
    
    @abstractmethod
    def post_response(self, data: list, input_text: str) -> str:
        """Gera resposta usando o modelo de linguagem"""
        pass

class Departamento(BuscaGeral):

    @traceable
    def search_embedding(input):

        embedding = embedding_m.get_embeddings(input)

        SCRIPT_SQL = sql_text(f"""
            SELECT id_departamento, cosine_distance(embedding, '{embedding}') AS cosine_dist
            FROM embedding_departamento
            WHERE embedding IS NOT NULL
            ORDER BY cosine_dist ASC
            LIMIT 5;
        """)
        registro = db.consult_db(SCRIPT_SQL) 
    
        data_frame = pd.DataFrame(registro, columns=['id_departamento', 'cosine_dist'])
        print(data_frame)

        Departamento.get_data(data_frame, input)
        return data_frame
    
    @traceable
    def get_data(data_frame, input):

        # os dados dos funcionarios são confusa usar o departamento depois
        departamento_data = []

        for row in data_frame.itertuples(index=False):
            id_departamento = row[0]
            #cosine_similarity = row[1]

            SCRIPT = sql_text(f"""
                SELECT id_departamento, nome_departamento, sigla, num_funcionarios
                FROM departamento
                WHERE id_departamento = {id_departamento}
            """)
            registro = db.consult_db(script=SCRIPT)
            data_frame = pd.DataFrame(registro, columns=[ 'id_departamento', 'nome_departamento', 'sigla', 'num_funcionarios'])
            
            # adiciona a similaridade ao dicionário
            #funcionario_dict = data_frame.iloc[0].to_dict()
            #funcionario_dict['relevancia'] = f"{cosine_similarity:.2f}"
            
            departamento_data.append(data_frame)
            # funcionarios_data.append(data_frame)

        print(departamento_data)
        Departamento.post_response(departamento_data, input)

        return departamento_data

    @traceable
    def post_response(departamento_data, input):
        docs = departamento_data
        # print(docs)
        PROMPT = f"""Você é um assistente de uma loja de móveis que ajuda funcionários com informações internas da empresa.

        Seu papel é analisar os dados fornecidos abaixo (em formato de dicionário/tabela) e responder à pergunta do usuário de forma clara, amigável e objetiva.

        Diretrizes:
        - Use apenas as informações presentes nos dados fornecidos.
        - Não invente informações ou faça suposições.
        - Se não houver informação suficiente para responder, diga claramente que não sabe.
        - Responda de forma natural, como se estivesse ajudando um colega de trabalho.
        - Evite termos muito técnicos ou respostas robóticas.

        Dados disponíveis:
        {docs}

        Pergunta do usuário:
        {input}

        Resposta:"""
        response = model.invoke(PROMPT)
        print(response)
        with open('respostas.txt', 'a') as f:
            f.write(f'{response}\n\n')

        return response

class Funcionario(BuscaGeral):
    
    @traceable
    def search_embedding(input):
        embedding = embedding_m.get_embeddings(input)

        SCRIPT_SQL = sql_text(f"""
            SELECT id_funcionario_ref, cosine_distance(embedding, '{embedding}') AS cosine_dist
            FROM embedding_funcionario
            WHERE embedding IS NOT NULL
            ORDER BY cosine_dist ASC
            LIMIT 5;
        """)
        registro = db.consult_db(SCRIPT_SQL) # erro aqui a tabela de embedding_funcionario não tem dados 
        data_frame = pd.DataFrame(registro, columns=['id_funcionario', 'cosine_dist'])
        print(data_frame)

        Funcionario.get_data(data_frame, input)
        return data_frame
    
    @traceable
    def get_data(data_frame, input):

        funcionario_data = []

        for row in data_frame.itertuples(index=False):
            id_funcinario_ref = row[0]
            #cosine_similarity = row[1]

            SCRIPT = sql_text(f"""
                SELECT id_funcionario, nome, cpf, endereco, contato
                FROM funcionario
                WHERE id_funcionario = {id_funcinario_ref}
            """)
            registro = db.consult_db(script=SCRIPT)
            data_frame = pd.DataFrame(registro, columns=[ 'id_funcionario', 'nome', 'cpf', 'endereco', 'contato'])
            
            # adiciona a similaridade ao dicionário
            #funcionario_dict = data_frame.iloc[0].to_dict()
            #funcionario_dict['relevancia'] = f"{cosine_similarity:.2f}"
            
            funcionario_data.append(data_frame)
            # funcionarios_data.append(data_frame)

        print(funcionario_data)
        Funcionario.post_response(funcionario_data, input)
        return funcionario_data
    

    @traceable
    def post_response(funcionario_data, input):
        docs = funcionario_data
        # print(docs)
        PROMPT = f"""Você é um assistente de uma loja de móveis que ajuda funcionários com informações internas da empresa.

        Seu papel é analisar os dados fornecidos abaixo (em formato de dicionário/tabela) e responder à pergunta do usuário de forma clara, amigável e objetiva.

        Diretrizes:
        - Use apenas as informações presentes nos dados fornecidos.
        - Não invente informações ou faça suposições.
        - Se não houver informação suficiente para responder, diga claramente que não sabe.
        - Responda de forma natural, como se estivesse ajudando um colega de trabalho.
        - Evite termos muito técnicos ou respostas robóticas.

        Dados disponíveis:
        {docs}

        Pergunta do usuário:
        {input}

        Resposta:"""
        response = model.invoke(PROMPT)
        print(response.content)
        with open('respostas.txt', 'a') as f:
            f.write(f'{response.content}\n\n')

        return response
    
class Produto(BuscaGeral):
    
    @traceable
    def search_embedding(entrada):
        input = entrada
        embedding = embedding_m.get_embeddings(input)

        print("EMBEDDING:", embedding)
        print("TYPE:", type(embedding))

        if embedding is None:
            raise ValueError("Embedding veio None — erro antes da query")
        

        embedding_str = "[" + ",".join(map(str, embedding)) + "]"
        SCRIPT = sql_text(f"""
    SELECT id_produto_ref, cosine_distance(embedding, '{embedding_str}') as cos_similarity
    FROM embedding_produto
    WHERE embedding IS NOT NULL
    ORDER BY cos_similarity ASC
    LIMIT 5
""")
        registro = db.consult_db(SCRIPT, {"embedding_str": embedding_str})
        data_frame = pd.DataFrame(registro, columns=['id_produto_ref', 'cos_similarity'])


        # if not registro:
        #     print("Nenhum resultado encontrado para o embedding")
        #     return pd.DataFrame()
        # else:
       #     print("Resultados encontrados para o embedding")
        #    print(f"Resultados: {registro}")

        Produto.get_data(data_frame, input)
        return data_frame

    @traceable
    def get_data(data_frame, input):

        data_produto = []

        for row in data_frame.itertuples(index=False):
            id_produto_ref = row[0]
            SCRIPT = sql_text(f"""SELECT DISTINCT * FROM produto
                                WHERE id_produto = {id_produto_ref}
            """)

            registro = db.consult_db(SCRIPT)
            len(registro)

            data_frame = pd.DataFrame(registro, columns=['id_produto', 'nome', 'marca', 'id_setor', 'preco_unitario'])
            data_frame.shape
            data_produto.append(data_frame)

#        print(data_produto)
        if data_produto:
            Produto.post_response(data_produto, input)

        return data_produto
    
    @traceable
    def post_response(data_produto, input_user):
        input = input_user
        docs = data_produto
                # print(docs)
        PROMPT = f"""Você é um assistente de uma loja de móveis que ajuda funcionários com informações internas da empresa.

        Seu papel é analisar os dados fornecidos abaixo (em formato de dicionário/tabela) e responder à pergunta do usuário de forma clara, amigável e objetiva.

        Diretrizes:
        - Use apenas as informações presentes nos dados fornecidos.
        - Não invente informações ou faça suposições.
        - Se não houver informação suficiente para responder, diga claramente que não sabe.
        - Responda de forma natural, como se estivesse ajudando um colega de trabalho.
        - Evite termos muito técnicos ou respostas robóticas.

        Dados disponíveis:
        {docs}

        Pergunta do usuário:
        {input}

        Resposta:"""


        response = model.invoke(PROMPT)
       # print(response.content)
        with open('respostas.txt', 'a') as f:
            f.write(f'{response.content}\n\n')

        return response

