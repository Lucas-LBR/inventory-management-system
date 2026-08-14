import csv
import os


PASTA_PROJETO = os.path.dirname(
    os.path.abspath(__file__)
)

ARQUIVO_CSV = os.path.join(
    PASTA_PROJETO,
    "produtos.csv"
)


COLUNAS = [
    "nome",
    "quantidade",
    "valor_unitario",
    "subtotal"
]


def ler_nome(mensagem):
    while True:
        nome = input(mensagem).strip()

        if nome != "":
            return nome

        print("O nome não pode ficar vazio.")


def ler_quantidade(mensagem):
    while True:
        try:
            quantidade = int(input(mensagem))

            if quantidade <= 0:
                print("Digite uma quantidade maior que zero.")
            else:
                return quantidade

        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")


def ler_valor(mensagem):
    while True:
        try:
            entrada = input(mensagem)
            entrada = entrada.replace(",", ".")

            valor = float(entrada)

            if valor <= 0:
                print("Digite um valor maior que zero.")
            else:
                return valor

        except ValueError:
            print("Entrada inválida. Digite somente números.")


def criar_produto(nome, quantidade, valor_unitario):
    subtotal = quantidade * valor_unitario

    produto = {
        "nome": nome,
        "quantidade": quantidade,
        "valor_unitario": valor_unitario,
        "subtotal": subtotal
    }

    return produto


def criar_produto_do_teclado():
    print("\n=== CADASTRO DE PRODUTO ===")

    nome = ler_nome("Nome do produto: ")
    quantidade = ler_quantidade("Quantidade: ")
    valor_unitario = ler_valor(
        "Valor unitário: R$ "
    )

    produto = criar_produto(
        nome,
        quantidade,
        valor_unitario
    )

    return produto


def salvar_produtos_csv(produtos):
    with open(
        ARQUIVO_CSV,
        mode="w",
        encoding="utf-8-sig",
        newline=""
    ) as arquivo:

        escritor = csv.DictWriter(
            arquivo,
            fieldnames=COLUNAS,
            delimiter=";"
        )

        escritor.writeheader()
        escritor.writerows(produtos)

    print("Produtos salvos com sucesso!")


def adicionar_produto_csv(produto):
    with open(
        ARQUIVO_CSV,
        mode="a",
        encoding="utf-8-sig",
        newline=""
    ) as arquivo:

        escritor = csv.DictWriter(
            arquivo,
            fieldnames=COLUNAS,
            delimiter=";"
        )

        escritor.writerow(produto)

    print("Novo produto adicionado com sucesso!")


def ler_produtos_csv():
    produtos = []

    with open(
        ARQUIVO_CSV,
        mode="r",
        encoding="utf-8-sig",
        newline=""
    ) as arquivo:

        leitor = csv.DictReader(
            arquivo,
            delimiter=";"
        )

        for linha in leitor:
            produto = criar_produto(
                linha["nome"],
                int(linha["quantidade"]),
                float(linha["valor_unitario"])
            )

            produtos.append(produto)

    return produtos


def alterar_preco_csv(nome_procurado):
    produtos = ler_produtos_csv()

    for produto in produtos:
        if produto["nome"].lower() == nome_procurado.lower():
            novo_preco = ler_valor(
                "Digite o novo preço: R$ "
            )

            produto["valor_unitario"] = novo_preco
            produto["subtotal"] = (
                produto["quantidade"] * novo_preco
            )

            salvar_produtos_csv(produtos)
            print("Preço alterado com sucesso!")
            return

    print("Produto não encontrado.")


def excluir_produto_csv(nome_procurado):
    produtos = ler_produtos_csv()

    for produto in produtos:
        if produto["nome"].lower() == nome_procurado.lower():
            produtos.remove(produto)

            salvar_produtos_csv(produtos)
            print("Produto excluído com sucesso!")
            return

    print("Produto não encontrado.")


def exibir_produtos():
    produtos = ler_produtos_csv()
    total_geral = 0

    print("\n=== PRODUTOS CADASTRADOS ===")

    if len(produtos) == 0:
        print("Nenhum produto cadastrado.")
        return

    for produto in produtos:
        print(
            f"{produto['nome']} — "
            f"{produto['quantidade']} unidades — "
            f"R$ {produto['valor_unitario']:.2f} cada — "
            f"Subtotal: R$ {produto['subtotal']:.2f}"
        )

        total_geral += produto["subtotal"]

    print(f"\nTotal geral: R$ {total_geral:.2f}")
def movimentar_estoque(nome_procurado, operacao):
    produtos = ler_produtos_csv()

    if operacao not in ["e", "s"]:
        print("Operação inválida.")
        return

    for produto in produtos:
        if produto["nome"].lower() == nome_procurado.lower():
            quantidade_movimento = ler_quantidade(
                "Digite a quantidade: "
            )

            if operacao == "e":
                produto["quantidade"] += quantidade_movimento
                mensagem = "Entrada registrada com sucesso!"

            else:
                if quantidade_movimento > produto["quantidade"]:
                    print("Estoque insuficiente.")
                    return

                produto["quantidade"] -= quantidade_movimento
                mensagem = "Saída registrada com sucesso!"

            produto["subtotal"] = (
                produto["quantidade"]
                * produto["valor_unitario"]
            )

            salvar_produtos_csv(produtos)
            print(mensagem)
            print(
                f"Estoque atual: "
                f"{produto['quantidade']} unidades"
            )
            return

    print("Produto não encontrado.")
def exibir_estoque_baixo():
    produtos = ler_produtos_csv()
    produtos_encontrados = 0

    print("\n=== ALERTA DE ESTOQUE BAIXO ===")

    for produto in produtos:
        if produto["quantidade"] <= 5:
            print(
                f"{produto['nome']} — "
                f"restam {produto['quantidade']} unidades"
            )

            produtos_encontrados += 1

    if produtos_encontrados == 0:
        print("Nenhum produto com estoque baixo.")
# NOVA FUNÇÃO:
# Cria o CSV somente se ele ainda não existir.
def inicializar_arquivo():
    if os.path.exists(ARQUIVO_CSV):
        print("Arquivo existente carregado.")
        return

    produtos_iniciais = [
        criar_produto("Bolo", 2, 50.0),
        criar_produto("Café", 3, 8.0)
    ]

    salvar_produtos_csv(produtos_iniciais)
    print("Arquivo criado pela primeira vez.")


def main():
    # LINHA ATUALIZADA:
    # Não apaga mais o arquivo a cada execução.
    inicializar_arquivo()

    novo_produto = criar_produto_do_teclado()
    adicionar_produto_csv(novo_produto)

    nome_alterar = ler_nome(
        "\nQual produto deseja alterar? "
    )
    alterar_preco_csv(nome_alterar)

    nome_excluir = ler_nome(
        "\nQual produto deseja excluir? "
    )
    excluir_produto_csv(nome_excluir)

    exibir_produtos()


if __name__ == "__main__":
    main()
