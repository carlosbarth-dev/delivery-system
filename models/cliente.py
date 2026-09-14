class Cliente:
    def __init__(self, id_cliente, nome, telefone, email=None):
        self.id_cliente = id_cliente
        self.nome = nome
        self.telefone = telefone
        self.email = email