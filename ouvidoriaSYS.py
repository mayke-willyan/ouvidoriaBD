from operacoesbd import *

categorias = ["Elogio", "Sugestão", "Reclamação"]

def print_cod_desc(reclamacoes):
    try:
        for item in reclamacoes:
            print(f" 🆔 ID: {item[0]} | 📄 DESCRIÇÃO: {item[2]}")

    except Exception as erro:
        print(f"\n[ERRO] falha ao formatar exibição simplificada {erro}")

def print_reclamacoes(reclamacoes):
    try:
        for reclamacao in reclamacoes:
            print(f"🔹 CÓDIGO:    {reclamacao[0]}")
            print(f"🔸 CATEGORIA: {reclamacao[1]}")
            print(f"📝 DESCRIÇÃO: {reclamacao[2]} \n")

    except Exception as erro:
        print(f"\n[ERRO] falha ao formatar exibição detalhada:  {erro}")

def listar_categorias_reclamacoes(categorias):
    try:
        print("\n--- CATEGORIAS DISPONÍVEIS ---")
        count = 0
        for categoria in categorias:
            print(f" {count + 1}) {categoria}")
            count += 1
        print("-" * 30)

    except Exception as erro:
        print(f"\n[ERRO] falha ao listar categorias: {erro}")

def listar_reclamacoes(connection):
    try:
        comando_bd = 'SELECT * FROM reclamacoes'
        reclamacoes = listarBancoDados(connection, comando_bd)

        print("\n" + "=" * 50)
        print(f"{'LISTAGEM DE MANIFESTAÇÕES':^50}")
        print("=" * 50)

        if not reclamacoes or len(reclamacoes) == 0:
            print("\n>>> Não existe nenhum item registrado no sistema.\n")
        else:
            print_reclamacoes(reclamacoes)
            print("-" * 50)

    except Exception as erro:
        print(f"\n[ERRO] falha ao processar listagem: {erro}")

def inserir_reclamacoes(connection):

    try:
        print("\n>>> INICIAR NOVO REGISTRO")
        listar_categorias_reclamacoes(categorias)

        entrada = input("Selecione o número da categoria: ")

        if entrada.isdigit():
            opcao_categoria = int(entrada)

            # Validação do intervalo da lista
            if 1 <= opcao_categoria <= len(categorias):
                categoria_escolhida = categorias[opcao_categoria - 1]
                descricao = input(f"Digite o relato do seu {categoria_escolhida}: ")

                commando_bd = 'INSERT INTO reclamacoes (categoria,descricao) values (%s,%s)'
                dados = (categoria_escolhida, descricao)

                resultado = insertNoBancoDados(connection,commando_bd,dados)

                if resultado is not None:
                    print(f"\n✅ {categoria_escolhida} registrado com sucesso!\n")
            else:
                print("\n[ERRO] Esta categoria não existe!")
        else:
            print("\n[ERRO] Digite apenas o número da opção!")

    except Exception as erro:
        print(f"\n[ERRO] Ocorreu um problema ao inserir: {erro}")

def pesquisar_reclamacoes(connection):
    try:
        print("\n>>> PESQUISAR POR CATEGORIA")
        listar_categorias_reclamacoes(categorias)

        entrada = input("Selecione a categoria para filtrar: ")

        if entrada.isdigit():
            opcao_categoria = int(entrada)

            if 1 <= opcao_categoria <= len(categorias):
                categoria_escolhida = categorias[opcao_categoria - 1]
                comando_bd = 'SELECT * from reclamacoes where categoria = %s'
                dados = [categoria_escolhida]
                reclamacoes = listarBancoDados(connection, comando_bd, dados)

                if reclamacoes and len(reclamacoes) > 0:
                    print(f"\n--- RESULTADOS PARA: {categoria_escolhida.upper()} ---")
                    print_cod_desc(reclamacoes)
                    print("-" * 40)

                else:
                    print(f"\n⚠️ Nenhum item encontrado na categoria: {categoria_escolhida}\n")
            else:
                print("\n[ERRO] Categoria inválida!")
        else:
            print("\n[ERRO] Entrada inválida! Digite o número da categoria.")

    except Exception as erro:
        print(f"\n[ERRO] Falha na pesquisa: {erro}")

def update_reclamacao(connection):
    try:

        listar_reclamacoes(connection)
        print("\n>>> ATUALIZAR REGISTRO")

        id_entrada = input("Digite o ID do item que deseja modificar: ")

        if id_entrada.isdigit():
            codigo_reclamacao = int(id_entrada)

            listar_categorias_reclamacoes(categorias)
            cat_entrada = input("Escolha a NOVA categoria (número): ")

            if cat_entrada.isdigit():
                opcao_categoria = int(cat_entrada)

                if 1 <= opcao_categoria <= len(categorias):
                    nova_categoria = categorias[opcao_categoria - 1]
                    nova_descricao = input("Digite a nova descrição detalhada: ")

                    comando_bd = "update reclamacoes set categoria = %s, descricao = %s where codigo = %s"
                    dados = [nova_categoria, nova_descricao, codigo_reclamacao]

                    linhas = atualizarBancoDados(connection, comando_bd, dados)

                    if linhas > 0:
                        print(f"\n✅ Registro {codigo_reclamacao} atualizado com sucesso!\n")
                    else:
                        print("\n[AVISO] Nenhuma alteração foi feita ou ID não encontrado.")

                else:
                    print("\n[ERRO] Categoria inválida!")
            else:
                print("\n[ERRO] Digite um número para a categoria!")
        else:
            print("\n[ERRO] O ID deve ser um número!")

    except Exception as erro:
        print(f"\n[ERRO] Falha ao atualizar: {erro}")

def remover_reclamacao(connection):
    try:

        listar_reclamacoes(connection)
        print("\n>>> REMOVER REGISTRO")

        entrada = input("Digite o ID do item que deseja EXCLUIR: ")

        if entrada.isdigit():
            codigo_reclamacao = int(entrada)

            # Adicionei uma pequena confirmação aqui, opcional mas segura
            confirmar = input(f"Tem certeza que deseja apagar o ID {codigo_reclamacao}? (S/N): ").upper()

            if confirmar == 'S':
                codigo_bd = "delete from reclamacoes where codigo = %s"
                dados = [codigo_reclamacao]
                linhas_afetadas = excluirBancoDados(connection, codigo_bd, dados)

                if linhas_afetadas == 0:
                    print(f"\n[!] Não existem itens com o código {codigo_reclamacao}.\n")
                else:
                    print("\n🗑️ Item removido do sistema com sucesso!\n")
            else:
                print("\nOperação de remoção cancelada.\n")
        else:
            print("\n[ERRO] Digite um código de ID válido (número)!\n")

    except Exception as e:
        print(f"\n[ERRO] Falha ao remover registro: {e}")

def listar_quantidade(connection):

    try:

        print("\n" + "-" * 30)
        print("1) Listar todas as reclamações")
        print("2) Listar por categoria específica")
        print("-" * 30)

        entrada = input("Escolha: ")

        if entrada.isdigit():
            opcao = int(entrada)

            if opcao == 1:
                listar_reclamacoes(connection)
            elif opcao == 2:
                listar_categorias_reclamacoes(categorias)

                cat_entrada = input("Escolha a categoria (número): ")

                if cat_entrada.isdigit():
                    opcao_categoria = int(cat_entrada)
                    if 1 <= opcao_categoria <= len(categorias):
                        categoria = categorias[opcao_categoria - 1]
                        codigo_bd = "select * from reclamacoes where categoria = %s"
                        reclamacoes = listarBancoDados(connection, codigo_bd, [categoria])

                        if len(reclamacoes) > 0:
                            print(f"\n--- TOTAL NA CATEGORIA {categoria.upper()}: {len(reclamacoes)} ---")
                            print_cod_desc(reclamacoes)
                        else:
                            print(f"\nNão há registros para {categoria}.")
                    else:
                        print("\n[ERRO] Categoria Inválida!")
                else:
                    print("\n[ERRO] Digite um número!")
            else:
                print("\n[ERRO] Opção de menu inválida.")
        else:
            print("\n[ERRO] Digite apenas números!")

    except Exception as e:
        print(f"\n[ERRO] Falha ao contabilizar registros: {e}")