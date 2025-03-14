palavras = {"feliz":"alegre"}

while True:
    print("\nMenu:")
    print("1 Adicionar palavara e sinonimo (chave e valor)")
    print("2 Remover palavra ")
    print("3 Ver itens no dicionário")
    print("4 Sair")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        chave = input("Digite a chave: ")
        valor = input("Digite o valor: ")
        palavras[chave] = chave = valor
        print(f'Item adicionado: "{chave}": "{valor}"')

    elif opcao == "2":
        chave = input("Digite a chave a ser removida: ")
        if chave in palavras:
            del palavras[chave]  # Remove a chave do dicionário
            print(f'Chave "{chave}:" removida com sucesso.')
        else:
            print("Chave não encontrada.")

    elif opcao == "3":
        if palavras:
            print("\nItens no dicionário:")
            for chave, valor in palavras.items():
                print(f"{chave}: {valor}")
        else:
            print("O dicionário está vazio.")

    elif opcao == "4":
        print("Saindo do programa...")
        break
    else:
        print("Opção inválida! Escolha uma opção de 1 a 4.")
