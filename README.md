# Exemplo de RAG com banco de dados e embeddings

Este projeto é um exemplo simples de como a tecnologia de RAG (Retrieval-Augmented Generation) pode ajudar empresas e pessoas a encontrar informações espalhadas em um banco de dados de forma mais natural e eficiente.

Em vez de consultar manualmente diversas tabelas e filtros, o sistema gera embeddings das informações, busca registros semanticamente semelhantes e envia apenas os dados relevantes para um modelo de linguagem. Isso reduz a fricção da consulta e torna a resposta mais contextualizada.

## Objetivo do exemplo

O objetivo aqui não é criar um produto pronto para produção, mas sim demonstrar o fluxo básico de um sistema RAG:

- armazenar informações em um banco relacional;
- transformar texto em embeddings;
- buscar os itens mais relevantes por similaridade;
- recuperar os registros relacionados;
- enviar esses dados para um modelo de linguagem;
- responder à pergunta do usuário com base em informações reais do banco.

Essa abordagem pode ser útil para:

- equipes que precisam localizar informações de clientes, produtos ou departamentos sem navegar em vários relatórios;
- pessoas que desejam consultar dados internos de maneira mais simples e conversacional;
- empresas que precisam criar assistentes para suporte interno usando informações já existentes no banco de dados.

## Visão da arquitetura

A estrutura foi mantida simples para facilitar a compreensão do fluxo.

```text
rag/exe3/
├── main.py                 # ponto de entrada para uso do exemplo
├── requirements.txt        # dependências do projeto
├── respostas.txt  
├── agente/
│   ├── agent.py           # lógica principal do RAG e geração de respostas
├── database/
│   ├── db.py               # conexão com o banco e funções de consulta
│   ├── db_agent.py         # geração de embeddings das tabelas
│   └── models.py           # modelos SQLAlchemy das entidades
├── embedding/
│   └── embedding_m.py      # geração de embeddings com Ollama
├── utils/
│   └── adhoc.py           # scripts utilitários e auxiliares
└── .env.example            # exemplo de variáveis de ambiente
```

### Fluxo de execução

1. Os dados do banco são transformados em textos descritivos.
2. Esses textos são convertidos em embeddings.
3. A pergunta do usuário é convertida no mesmo formato de embedding.
4. O sistema compara a pergunta com os embeddings armazenados e identifica os mais próximos.
5. Os registros recuperados são enviados para o modelo de linguagem.
6. O modelo responde de forma contextualizada, usando apenas os dados retornados.

## Tecnologias usadas

- Python
- SQLAlchemy
- PostgreSQL com extensão pgvector
- Ollama embeddings
- LangChain
- Groq / modelos de linguagem
- dotenv para variáveis de ambiente

## Pré-requisitos

Antes de executar o projeto, verifique se você tem:

- Python 3.10+ instalado;
- PostgreSQL com a extensão pgvector habilitada;
- Ollama instalado e com o modelo de embedding disponível;
- uma chave de API do Groq configurada no ambiente.

## Configuração

Crie um arquivo `.env` baseado em `.env.example` e preencha os valores:

```env
DATABASE_URL="postgresql://usuario:senha@host:5432/nome_db"
GROQ_API_KEY="sua_chave"
```

É recomendado também configurar as variáveis de tracing do LangSmith, caso queira acompanhar chamadas e respostas do fluxo.

## Como executar

1. Crie um ambiente virtual e instale as dependências:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Verifique se o banco está acessível e as tabelas de embeddings existem.

3. Gere os embeddings das tabelas a partir do script em `database/db_agent.py`.

4. Execute o ponto de entrada principal:

```bash
python main.py
```

5. Escolha a tabela de consulta e escreva a pergunta.

## Exemplo de uso

O exemplo pode ser usado para perguntas como:

- "Quais produtos têm maior relação com móveis de escritório?"
- "Quem é o funcionário responsável por um determinado departamento?"
- "Quais dados de departamento estão relacionados a logística?"

Essas consultas são respondidas com base em registros do banco, usando busca por similaridade e geração de texto.

## Observações

Este repositório foi pensado como um estudo de conceito e como exemplo didático. Ele mostra um caminho simples para aplicar RAG em dados estruturados, sem abordar todas as complexidades de um sistema de produção.

A ideia central é demonstrar que a tecnologia pode transformar a experiência de busca e recuperação de informação, ajudando pessoas e empresas a acessar dados distribuídos de forma mais direta, rápida e compreensível.
