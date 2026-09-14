# Modelos

Mantidos: `Cliente`, `Categoria`, `Produto`, `Pedido` e `ItemPedido`.

- `Restaurante`: nome, taxa de entrega e ativo.
- `Categoria` e `Produto`: possuem `id_restaurante`.
- `Pedido`: cliente, restaurante, subtotal, taxa, total, modalidade, status, chave idempotente e datas.
- `ItemPedido`: produto, nome, quantidade e preço congelado na compra.
- `Payment`: tentativa de pagamento, método, valor, status, referência e chave idempotente.

Não foi criado model de entrega: modalidade e taxa pertencem ao pedido.
