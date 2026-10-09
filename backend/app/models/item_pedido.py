class ItemPedido:
    """Item do pedido com snapshot do preço no momento da compra."""

    def __init__(self, id_item, id_pedido, id_produto, quantidade, preco_unitario, nome_produto=None):
        self.id_item = id_item
        self.id_pedido = id_pedido
        self.id_produto = id_produto
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario
        self.nome_produto = nome_produto
