class Categoria:
    def __init__(self, id_categoria, nome, descricao=None, id_restaurante=None):
        self.id_categoria = id_categoria
        self.nome = nome
        self.descricao = descricao
        self.id_restaurante = id_restaurante
