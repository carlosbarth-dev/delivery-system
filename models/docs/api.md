# API Delivery

Inicie a API a partir da raiz do projeto:

```powershell
python -m uvicorn models.database.api.main:app --reload --port 8001
```

Endereços locais:

- `http://127.0.0.1:8001/` — rota inicial;
- `http://127.0.0.1:8001/health` — verificação de disponibilidade;
- `http://127.0.0.1:8001/docs` — documentação interativa.

## Fluxo do MVP

1. `POST /checkout`, com o cabeçalho `Idempotency-Key`, recebe cliente, restaurante,
   tipo de recebimento (`ENTREGA` ou `RETIRADA`) e itens. A API busca os preços no
   banco, calcula subtotal, taxa de entrega e total, e cria pedido e itens.
2. `POST /pagamentos`, também com `Idempotency-Key`, inicia uma tentativa de pagamento.
3. `PATCH /pagamentos/{id}` recebe o resultado (`APROVADO`, `RECUSADO` ou
   `CANCELADO`). Ao aprovar, o pedido passa para `CONFIRMADO`.
4. `PATCH /pedidos/{id}/status` avança o pedido até entrega ou retirada.

Uma chave de idempotência deve ser nova para cada operação e repetida somente ao
reenviar a mesma requisição. Com uma chave já usada, a API devolve o registro original.
