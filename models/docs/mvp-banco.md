# Banco e migração

Para banco novo, execute `database/delivery.sql`.

Para banco existente, execute `database/migrations/001_mvp_checkout.sql`:

1. Crie ou escolha o restaurante dos dados legados.
2. Execute os `UPDATE`s de backfill indicados no arquivo.
3. Aplique as constraints finais comentadas no mesmo arquivo.

Novas tabelas: `restaurante` e `pagamento`. Novas relações ligam categoria, produto e pedido ao restaurante.
