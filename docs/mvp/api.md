# API do MVP de checkout

Inicie o backend a partir da raiz do repositorio:

```powershell
cd backend
python main.py
```

Enderecos locais:

- `http://localhost:8000/` - rota inicial;
- `http://localhost:8000/health` - verificacao de disponibilidade;
- `http://localhost:8000/docs` - documentacao interativa.

## Fluxo

1. `POST /checkout` recebe cliente, restaurante, tipo de recebimento (`ENTREGA` ou `RETIRADA`) e itens. A API busca os precos no banco, calcula subtotal, taxa de entrega e total, e cria pedido e itens.
2. `POST /pagamentos` inicia uma tentativa de pagamento.
3. `PATCH /pagamentos/{id}` recebe o resultado (`APROVADO`, `RECUSADO` ou `CANCELADO`). Ao aprovar, o pedido passa para `CONFIRMADO`.
4. `PATCH /pedidos/{id}/status` avanca o pedido ate entrega ou retirada.

Checkout e criacao de pagamento exigem o cabecalho `Idempotency-Key`. Repita uma chave somente ao reenviar a mesma solicitacao.

Consulte [endpoints.md](./endpoints.md) para o catalogo de rotas e [API.md](../API.md) para o contrato-alvo completo do projeto.
