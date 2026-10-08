from sqlalchemy import Column, ForeignKey, Integer, Numeric, VARCHAR
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from pgvector.sqlalchemy import Vector

from db import engine


Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Setor(Base):
    __tablename__ = "setor"

    id_setor = Column(Integer, primary_key=True)
    nome = Column(VARCHAR(100), nullable=False)


class Produto(Base):
    __tablename__ = "produto"

    id_produto = Column(Integer, primary_key=True)
    nome = Column(VARCHAR(100), nullable=False)
    marca = Column(VARCHAR(100), nullable=False)
    id_setor = Column(ForeignKey("setor.id_setor"), nullable=False)
    preco_unitario = Column(Numeric(10, 2), nullable=False)

    setor = relationship("Setor")


class Departamento(Base):
    __tablename__ = "departamento"

    id_departamento = Column(Integer, primary_key=True)
    nome_departamento = Column(VARCHAR(100), nullable=False)
    sigla = Column(VARCHAR(10), nullable=False)
    num_funcionarios = Column(Integer, nullable=False)


class Funcionario(Base):
    __tablename__ = "funcionario"

    id_funcionario = Column(Integer, primary_key=True)
    id_departamento = Column(Integer, ForeignKey("departamento.id_departamento"), nullable=False)
    nome = Column(VARCHAR(100), nullable=False)
    cpf = Column(VARCHAR(100), nullable=False)
    endereco = Column(VARCHAR(100))
    contato = Column(VARCHAR(100), nullable=False)

    departamento = relationship("Departamento")


class Cliente(Base):
    __tablename__ = "cliente"

    id_cliente = Column(Integer, primary_key=True)
    nome = Column(VARCHAR(100), nullable=False)
    contato = Column(VARCHAR(100), nullable=False)
    endereco = Column(VARCHAR(100), nullable=False)
    cpf = Column(VARCHAR(100))


class Vendas(Base):
    __tablename__ = "vendas"

    id_venda = Column(Integer, primary_key=True)
    id_funcionario = Column(ForeignKey("funcionario.id_funcionario"), nullable=False)
    id_cliente = Column(ForeignKey("cliente.id_cliente"), nullable=False)
    id_produto = Column(ForeignKey("produto.id_produto"), nullable=False)
    quantidade = Column(Integer, nullable=False)

    funcionario = relationship("Funcionario")
    cliente = relationship("Cliente")
    produto = relationship("Produto")


class EmbeddingFuncionario(Base):
    __tablename__ = "embedding_funcionario"

    id_funcionario_ref = Column(Integer, primary_key=True)
    embedding = Column(Vector(1024), nullable=False)

    funcionario = relationship("Funcionario")


class EmbeddingProduto(Base):
    __tablename__ = "embedding_produto"

    id_produto_ref = Column(Integer, primary_key=True)
    embedding = Column(Vector(1024), nullable=False)

    produto = relationship("Produto")


class EmbeddingSetor(Base):
    __tablename__ = "embedding_setor"

    id_setor = Column(Integer, primary_key=True)
    embedding = Column(Vector(1024))


class EmbeddingDepartamento(Base):
    __tablename__ = "embedding_departamento"

    id_departamento = Column(Integer, primary_key=True)
    embedding = Column(Vector(1024))


Base.metadata.create_all(engine)

