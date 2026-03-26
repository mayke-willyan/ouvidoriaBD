from ouvidoriaSYS import *

# Sugestão: Verifique se o nome do banco 'ouvidoriap2' está correto no seu MySQL
connection = criarConexao("localhost","root","Mayke@A1223145","ouvidoriap2")

while True:
    print("\n" + "="*50)
    print(f"{'SISTEMA DE OUVIDORIA UNIVERSITÁRIA':^50}")
    print("="*50)
    print("""
    [1] Listar Reclamações Registradas
    [2] Registrar uma nova Reclamação
    [3] Pesquisar uma Reclamação pela categoria
    [4] Atualizar uma Reclamação existente
    [5] Remover uma Reclamação pelo código
    [6] Mostrar a Quantidade de reclamações cadastradas
    [7] Sair
    """)
    print("-" * 50)

    entrada = int(input("Escolha uma das opções: "))

    if entrada.is_integer():

        opcao = int(entrada)

        if opcao == 7:
            print("\nEncerrando o sistema... Até logo!")
            break

        elif opcao == 1:
            listar_reclamacoes(connection)

        elif opcao == 2:
            inserir_reclamacoes(connection)

        elif opcao == 3:
            pesquisar_reclamacoes(connection)

        elif opcao == 4:
            update_reclamacao(connection)

        elif opcao == 5:
            remover_reclamacao(connection)

        elif opcao == 6:
            listar_quantidade(connection)

encerrarConexao(connection)