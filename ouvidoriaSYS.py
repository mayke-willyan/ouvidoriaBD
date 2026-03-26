from operacoesbd import *

categorias = ["Elogio", "Sugestão", "Reclamação"]


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
        for reclamacao in reclamacoes:
            print(f"🔹 CÓDIGO:    {reclamacao[0]}")
            print(f"🔸 CATEGORIA: {reclamacao[1]}")
            print(f"📝 DESCRIÇÃO: {reclamacao[2]}")
            print("-" * 50)


def inserir_reclamacoes(connection):
    commando_bd = 'INSERT INTO reclamacoes (categoria,descricao) values (%s,%s)'

    print("\n>>> INICIAR NOVO REGISTRO")
    listar_categorias_reclamacoes(categorias)

    opcao_categoria = int(input("Selecione o número da categoria: "))

    # Nota: Aqui pode dar erro se o usuário digitar um número fora do range (Ex: 5)
    categoria_escolhida = categorias[opcao_categoria - 1]

    if categoria_escolhida not in categorias:
        print("\n[ERRO] Categoria escolhida não existe!")
    else:
        descricao = input(f"Digite o relato do seu {categoria_escolhida}: ")
        dados = (categoria_escolhida, descricao)
        insertNoBancoDados(connection, commando_bd, dados)
        print(f"\n✅ {categoria_escolhida} registrado com sucesso!\n")


def pesquisar_reclamacoes(connection):
    print("\n>>> PESQUISAR POR CATEGORIA")
    listar_categorias_reclamacoes(categorias)

    opcao_categoria = int(input("Selecione a categoria para filtrar: "))
    categoria_escolhida = categorias[opcao_categoria - 1]

    comando_bd = 'SELECT * from reclamacoes where categoria = %s'
    dados = [categoria_escolhida]

    reclamacoes = listarBancoDados(connection, comando_bd, dados)

    if len(reclamacoes) > 0:
        print(f"\n--- RESULTADOS PARA: {categoria_escolhida.upper()} ---")
        for item in reclamacoes:
            print(f" 🆔 ID: {item[0]} | 📄 DESCRIÇÃO: {item[2]}")
        print("-" * 40)
    else:
        print(f"\n⚠️ Nenhum item encontrado na categoria: {categoria_escolhida}\n")


def update_reclamacao(connection):
    listar_reclamacoes(connection)

    print("\n>>> ATUALIZAR REGISTRO")
    codigo_reclamacao = int(input("Digite o ID do item que deseja modificar: "))

    listar_categorias_reclamacoes(categorias)
    print("**** Escolha a NOVA categoria ****")
    opcao_categoria = int(input("Número: "))

    if opcao_categoria < 1 or opcao_categoria > len(categorias):
        print("\n[ERRO] Categoria Inválida! Operação cancelada.")
        return

    comando_bd = "update reclamacoes set categoria = %s, descricao = %s where codigo = %s"

    nova_categoria = categorias[opcao_categoria - 1]
    nova_descricao = input("Digite a nova descrição detalhada: ")

    dados = [nova_categoria, nova_descricao, codigo_reclamacao]
    atualizarBancoDados(connection, comando_bd, dados)

    print(f"\n✅ {nova_categoria} atualizado com sucesso!\n")


def remover_reclamacao(connection):
    listar_reclamacoes(connection)

    print("\n>>> REMOVER REGISTRO")
    codigo_reclamacao = int(input("Digite o ID do item que deseja EXCLUIR: "))

    codigo_bd = "delete from reclamacoes where codigo = %s"
    dados = [codigo_reclamacao]

    linhas_afetadas = excluirBancoDados(connection, codigo_bd, dados)

    if linhas_afetadas == 0:
        print(f"\n[!] Não existem itens com o código {codigo_reclamacao}.\n")
    else:
        print("\n🗑️ Item removido do sistema com sucesso!\n")


def listar_quantidade(connection):
    print("\n" + "-" * 30)
    print("1) Listar todas as reclamações")
    print("2) Listar por categoria específica")
    print("-" * 30)

    opcao = int(input("Escolha: "))

    # Nota: A condição '0 < opcao > 2' no seu original está um pouco confusa.
    if opcao < 1 or opcao > 2:
        print("\n[!] Opção não existe no menu de quantidade.")
        return

    elif opcao == 1:
        listar_reclamacoes(connection)

    elif opcao == 2:
        listar_categorias_reclamacoes(categorias)
        opcao_categoria = int(input("Escolha a categoria: "))

        if opcao_categoria < 1 or opcao_categoria > len(categorias):
            print("\n[ERRO] Categoria Inválida!")
            return

        codigo_bd = "select * from reclamacoes where categoria = %s"
        categoria = categorias[opcao_categoria - 1]

        # Nota: faltava chamar a função de listar aqui
        reclamacoes = listarBancoDados(connection, codigo_bd, [categoria])

        for item in reclamacoes:
            print(f"🔹 CÓDIGO:    {item[0]}")
            print(f"🔸 CATEGORIA: {item[1]}")
            print(f"📝 DESCRIÇÃO: {item[2]}")
            print("-" * 50)
