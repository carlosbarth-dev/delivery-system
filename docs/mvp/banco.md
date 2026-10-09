# Banco e migração

Para banco novo, execute [`backend/database/schema.sql`](../../backend/database/schema.sql).

Para banco existente, execute [`backend/database/migrations/001_mvp_checkout.sql`](../../backend/database/migrations/001_mvp_checkout.sql):

1. Crie ou escolha o restaurante dos dados legados.
2. Execute os `UPDATE`s de backfill indicados no arquivo.
3. Aplique as constraints finais comentadas no mesmo arquivo.
O backfill evita atribuir silenciosamente pedidos legados a um restaurante incorreto.

Novas tabelas: `restaurante` e `pagamento`. Novas relações ligam categoria, produto e pedido ao restaurante.

O banco esperado é `delivery_db`, igual ao Docker Compose. Aplique a migração ao banco selecionado e revise os passos de backfill e constraints antes de executá-la em dados existentes.
