from agent import Produto, Departamento, Funcionario
from dotenv import load_dotenv 


def pesquisa(input_user):

    if input_user not in search_type:
            print('não posso te ajudar infelizmente')
    
    else:
        if input_user == 'produto':
            entrada = str(input('digite sua pergunta: '))
            Produto.search_embedding(entrada)
        
        elif input_user == 'departamento':
            entrada = str(input('digite sua pergunta: '))
            Departamento.search_embedding(entrada)

        elif input_user == 'funcionario':
            entrada = str(input('digite sua pergunta: '))
            Funcionario.search_embedding(entrada)

        else:
            print('nao existem informações sobre o que voce deseja saber, sinto muito')
    
if __name__ == '__main__':


    load_dotenv()
    search_type = ['produto', 'departamento', 'funcionario']
    input_user = str(input('qual tabela voce quer analisar?: '))
    pesquisa(input_user)
