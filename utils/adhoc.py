
from models import Setor, Produto, Funcionario, Cliente, Departamento, Vendas
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func, distinct
from db import engine


# count funcionario
def count_funcionario(db):
    num_func = db.query(func.count(distinct(Produto.id_produto))).all()
    print(num_func)
    return num_func

# count departamento

def count_dep(db):
    num_dep = db.query(func.count(distinct(Departamento.id_departamento))).all()

    return num_dep




# count setores



# count clientes



# count Departamento


if __name__ == '__main__':

    Session = sessionmaker(bind=engine)
    db = Session()
    count_funcionario(db)