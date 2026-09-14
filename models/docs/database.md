## Atualização do MVP

Para uma instalação nova, execute `database/delivery.sql`. Para uma base criada
antes do MVP, execute primeiro `database/migrations/001_mvp_checkout.sql`, faça o
backfill indicado no arquivo e só então aplique as constraints finais. Isso evita
atribuir silenciosamente os pedidos legados a um restaurante incorreto.
