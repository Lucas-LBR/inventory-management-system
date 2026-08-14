from sistema_produtos import (
    inicializar_arquivo,
    criar_produto_do_teclado,
    adicionar_produto_csv,
    exibir_produtos,
    alterar_preco_csv,
    excluir_produto_csv,
    exibir_estoque_baixo,
    movimentar_estoque,
    ler_nome
)


def mostrar_menu():
    print("\n=== SISTEMA DE ESTOQUE ===")
    print("1 - Cadastrar produto")
    print("2 - Listar produtos")
    print("3 - Alterar preço")
    print("4 - Excluir produto")
    print("5 - Ver estoque baixo")
    print("6 - Registrar entrada ou saída")
    print("7 - Sair")

    return input("\nEscolha uma opção: ").strip()


def main():
    inicializar_arquivo()

    while True:
        opcao = mostrar_menu()

        if opcao == "1":
            produto = criar_produto_do_teclado()
            adicionar_produto_csv(produto)

        elif opcao == "2":
            exibir_produtos()

        elif opcao == "3":
            nome = ler_nome(
                "\nQual produto deseja alterar? "
            )
            alterar_preco_csv(nome)

        elif opcao == "4":
            nome = ler_nome(
                "\nQual produto deseja excluir? "
            )

            confirmacao = input(
                f"Confirma a exclusão de '{nome}'? (s/n): "
            ).strip().lower()

            if confirmacao == "s":
                excluir_produto_csv(nome)
            else:
                print("Exclusão cancelada.")

        elif opcao == "5":
            exibir_estoque_baixo()

        elif opcao == "6":
            nome = ler_nome(
                "\nQual produto deseja movimentar? "
            )

            operacao = input(
                "Digite E para entrada ou S para saída: "
            ).strip().lower()

            movimentar_estoque(
                nome,
                operacao
            )

        elif opcao == "7":
            print("Programa encerrado.")
            break

        else:
            print("Opção inválida. Escolha de 1 a 7.")


if __name__ == "__main__":
    main()
    