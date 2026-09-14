-- Migração para um banco criado pelo delivery.sql antigo (MySQL 8.0.29+).
-- Faça backup antes de executar. Não execute as linhas de backfill sem ajustar o id do restaurante.
USE delivery;

CREATE TABLE IF NOT EXISTS restaurante (
    id_restaurante INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    taxa_entrega DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    ativo BOOLEAN NOT NULL DEFAULT TRUE
);

ALTER TABLE categoria ADD COLUMN IF NOT EXISTS id_restaurante INT NULL;
ALTER TABLE produto ADD COLUMN IF NOT EXISTS id_restaurante INT NULL;
ALTER TABLE pedido ADD COLUMN IF NOT EXISTS id_restaurante INT NULL;
ALTER TABLE pedido ADD COLUMN IF NOT EXISTS atualizado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;
ALTER TABLE pedido ADD COLUMN IF NOT EXISTS tipo_recebimento VARCHAR(15) NULL;
ALTER TABLE pedido ADD COLUMN IF NOT EXISTS subtotal DECIMAL(10,2) NOT NULL DEFAULT 0.00;
ALTER TABLE pedido ADD COLUMN IF NOT EXISTS taxa_entrega DECIMAL(10,2) NOT NULL DEFAULT 0.00;
ALTER TABLE pedido ADD COLUMN IF NOT EXISTS chave_idempotencia VARCHAR(100) NULL;
ALTER TABLE item_pedido ADD COLUMN IF NOT EXISTS nome_produto VARCHAR(100) NULL;

-- 1) Crie/cadastre um restaurante; 2) troque 1 pelo id correto; 3) remova os comentários:
-- INSERT INTO restaurante (nome, taxa_entrega) VALUES ('Restaurante padrão', 5.00);
-- UPDATE categoria SET id_restaurante = 1 WHERE id_restaurante IS NULL;
-- UPDATE produto SET id_restaurante = 1 WHERE id_restaurante IS NULL;
-- UPDATE pedido SET id_restaurante = 1, tipo_recebimento = 'ENTREGA', subtotal = valor_total,
--     chave_idempotencia = CONCAT('legado-pedido-', id_pedido)
--     WHERE id_restaurante IS NULL OR tipo_recebimento IS NULL OR chave_idempotencia IS NULL;
-- UPDATE item_pedido i JOIN produto p ON p.id_produto = i.id_produto
--     SET i.nome_produto = p.nome WHERE i.nome_produto IS NULL;

-- Após conferir o backfill, aplique as constraints abaixo manualmente (uma vez):
-- ALTER TABLE categoria MODIFY id_restaurante INT NOT NULL,
--   ADD CONSTRAINT fk_categoria_restaurante FOREIGN KEY (id_restaurante) REFERENCES restaurante(id_restaurante);
-- ALTER TABLE produto MODIFY id_restaurante INT NOT NULL,
--   ADD CONSTRAINT fk_produto_restaurante FOREIGN KEY (id_restaurante) REFERENCES restaurante(id_restaurante);
-- ALTER TABLE pedido MODIFY id_restaurante INT NOT NULL, MODIFY tipo_recebimento VARCHAR(15) NOT NULL,
--   MODIFY chave_idempotencia VARCHAR(100) NOT NULL,
--   ADD CONSTRAINT uq_pedido_idempotencia UNIQUE (chave_idempotencia),
--   ADD CONSTRAINT fk_pedido_restaurante FOREIGN KEY (id_restaurante) REFERENCES restaurante(id_restaurante);
-- ALTER TABLE item_pedido MODIFY nome_produto VARCHAR(100) NOT NULL;

CREATE TABLE IF NOT EXISTS pagamento (
    id_pagamento INT AUTO_INCREMENT PRIMARY KEY,
    id_pedido INT NOT NULL,
    metodo VARCHAR(30) NOT NULL,
    valor DECIMAL(10,2) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'PENDENTE',
    chave_idempotencia VARCHAR(100) NOT NULL,
    referencia_externa VARCHAR(100),
    criado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    atualizado_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT uq_pagamento_idempotencia UNIQUE (chave_idempotencia),
    CONSTRAINT fk_pagamento_pedido FOREIGN KEY (id_pedido) REFERENCES pedido(id_pedido)
);
