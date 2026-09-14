class Restaurante:
    def __init__(self, id_restaurante, nome, taxa_entrega=0.0, ativo=True):
        self.id_restaurante = id_restaurante
        self.nome = nome
        self.taxa_entrega = taxa_entrega
        self.ativo = ativo
