class Produto:
    def __init__(self, id_produto, id_categoria, nome, preco, disponivel=True, id_restaurante=None):
        self.id_produto = id_produto
        self.id_categoria = id_categoria
        self.nome = nome
        self.preco = preco
        self.disponivel = disponivel
        self.id_restaurante = id_restaurante
