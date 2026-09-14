-- Aplicar uma vez, DEPOIS de models/database/delivery.sql, em banco de teste.
-- Antes de aplicar em um banco com dados, faça backup e confira produtos existentes.
-- A coluna nova corresponde à descrição exibida pelo front do Nathan.

ALTER TABLE produto
    ADD COLUMN descricao VARCHAR(255) NULL;

-- MySQL 8.0.16+ aplica CHECK. Valores negativos existentes impedem a migração.
ALTER TABLE produto
    ADD CONSTRAINT ck_produto_preco_nao_negativo CHECK (preco >= 0);
