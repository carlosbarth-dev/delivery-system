
class ItemPedido:
    def __init__(self, id_item, id_pedido, id_produto, quantidade, preco_unitario):
        self.id_item = id_item
        self.id_pedido = id_pedido
        self.id_produto = id_produto
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario

        #crie uma classe intem pedido, depois que o cliente fazer o pedido 
        