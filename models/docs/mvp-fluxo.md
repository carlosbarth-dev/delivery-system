# Fluxo e idempotência

`Checkout` não é model: é o fluxo que cria pedido e itens em uma transação.

1. Cliente envia itens e modalidade.
2. API valida produtos, busca preços no banco e calcula subtotal, taxa e total.
3. API cria o pedido em `AGUARDANDO_PAGAMENTO`.
4. Pagamento aprovado confirma o pedido.
5. Pedido segue para preparo e entrega ou retirada.

`Idempotency-Key` é obrigatória em checkout e pagamento. A mesma chave devolve o registro já criado, impedindo duplicidade.
