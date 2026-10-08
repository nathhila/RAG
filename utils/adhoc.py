from sqlalchemy import distinct, func
from sqlalchemy.orm import sessionmaker

from db import engine
from models import Departamento, Produto


def count_funcionario(session):
    return session.query(func.count(distinct(Produto.id_produto))).all()


def count_dep(session):
    return session.query(func.count(distinct(Departamento.id_departamento))).all()


if __name__ == "__main__":
    session_factory = sessionmaker(bind=engine)
    session = session_factory()
    count_funcionario(session)
    count_dep(session)