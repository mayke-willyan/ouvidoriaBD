from operacoesbd import *

categorias = ["Elogio", "Sugestão", "Reclamação"]

def print_cod_desc(reclamacoes):
    for item in reclamacoes:
        print(f" 🆔 ID: {item[0]} | 📄 DESCRIÇÃO: {item[2]}")


def print_reclamacoes(reclamacoes):

    for reclamacao in reclamacoes:
        print(f"🔹 CÓDIGO:    {reclamacao[0]}")
        print(f"🔸 CATEGORIA: {reclamacao[1]}")
        print(f"📝 DESCRIÇÃO: {reclamacao[2]}")

def listar_categorias_reclamacoes(categorias):
    print("\n--- CATEGORIAS DISPONÍVEIS ---")
    count = 0
    for categoria in categorias:
        print(f" {count + 1}) {categoria}")
        count += 1
    print("-" * 30)


def listar_reclamacoes(connection):
    comando_bd = 'SELECT * FROM reclamacoes'
    reclamacoes = listarBancoDados(connection, comando_bd)

    print("\n" + "=" * 50)
    print(f"{'LISTAGEM DE MANIFESTAÇÕES':^50}")
    print("=" * 50)

    if len(reclamacoes) == 0:
        print("\n>>> Não existe nenhum item registrado no sistema.\n")
    else:
        print_reclamacoes(reclamacoes)
        print("-" * 50)

def inserir_reclamacoes(connection):
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
            insertNoBancoDados(connection, commando_bd, dados)
            print(f"\n✅ {categoria_escolhida} registrado com sucesso!\n")
        else:
            print("\n[ERRO] Esta categoria não existe!")
    else:
        print("\n[ERRO] Digite apenas o número da opção!")


def pesquisar_reclamacoes(connection):
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

            if len(reclamacoes) > 0:
                print(f"\n--- RESULTADOS PARA: {categoria_escolhida.upper()} ---")
                print_cod_desc(reclamacoes)
                print("-" * 40)
            else:
                print(f"\n⚠️ Nenhum item encontrado na categoria: {categoria_escolhida}\n")
        else:
            print("\n[ERRO] Categoria inválida!")
    else:
        print("\n[ERRO] Entrada inválida! Digite o número da categoria.")


def update_reclamacao(connection):
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
                atualizarBancoDados(connection, comando_bd, dados)
                print(f"\n✅ Registro {codigo_reclamacao} atualizado com sucesso!\n")
            else:
                print("\n[ERRO] Categoria inválida!")
        else:
            print("\n[ERRO] Digite um número para a categoria!")
    else:
        print("\n[ERRO] O ID deve ser um número!")


def remover_reclamacao(connection):
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


def listar_quantidade(connection):
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