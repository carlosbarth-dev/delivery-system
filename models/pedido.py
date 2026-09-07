class Pedido:
    def __init__(self, id_pedido, id_cliente, data_pedido, status="pendente", valor_total=0.0):
        self.id_pedido = id_pedido
        self.id_cliente = id_cliente
        self.data_pedido = data_pedido
        self.status = status
        self.valor_total = valor_total