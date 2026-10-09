# Endpoints MVP

| Método | Rota | Finalidade |
| --- | --- | --- |
| POST | `/checkout` | Cria checkout e pedido; exige `Idempotency-Key`. |
| GET | `/pedidos/{id}` | Consulta pedido e itens. |
| POST | `/pagamentos` | Inicia pagamento; exige `Idempotency-Key`. |
| PATCH | `/pagamentos/{id}` | Atualiza status do pagamento. |
| PATCH | `/pedidos/{id}/status` | Avança o status operacional. |

O checkout recebe `cliente_id`, `restaurante_id`, `tipo_recebimento` (`ENTREGA` ou `RETIRADA`) e uma lista `itens` com `produto_id` e `quantidade`. Os preços são consultados no banco. As rotas de pagamento e criação de checkout exigem `Idempotency-Key`.

Pedido: `AGUARDANDO_PAGAMENTO`, `CONFIRMADO`, `EM_PREPARO`, `PRONTO_PARA_RETIRADA`, `SAIU_PARA_ENTREGA`, `ENTREGUE`, `CANCELADO`.

Pagamento: `PENDENTE`, `APROVADO`, `RECUSADO`, `CANCELADO`.
