class Produto:
    def __init__(self, id_produto, id_categoria, nome, preco, disponivel=True):
        self.id_produto = id_produto
        self.id_categoria = id_categoria
        self.nome = nome
        self.preco = preco
        self.disponivel = disponivel