from agent import Departamento, Funcionario, Produto


SEARCH_TYPES = {"produto", "departamento", "funcionario"}


def pesquisa(input_user: str):
    if input_user not in SEARCH_TYPES:
        print("Tabela inválida. Escolha entre: produto, departamento ou funcionario.")
        return

    pergunta = input("Digite sua pergunta: ")

    if input_user == "produto":
        Produto.search_embedding(pergunta)
    elif input_user == "departamento":
        Departamento.search_embedding(pergunta)
    elif input_user == "funcionario":
        Funcionario.search_embedding(pergunta)


if __name__ == "__main__":
    tabela = input("Qual tabela você quer analisar? [produto/departamento/funcionario]: ").strip().lower()
    pesquisa(tabela)
