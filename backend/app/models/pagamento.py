from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional


class StatusPagamento(str, Enum):
    PENDENTE = "PENDENTE"
    APROVADO = "APROVADO"
    RECUSADO = "RECUSADO"
    CANCELADO = "CANCELADO"


class Payment:
    """Tentativa de pagamento associada a um pedido."""

    def __init__(self, id_pagamento, id_pedido, metodo, valor: Decimal,
                 status=StatusPagamento.PENDENTE, chave_idempotencia=None,
                 referencia_externa=None, criado_em: Optional[datetime] = None,
                 atualizado_em: Optional[datetime] = None):
        self.id_pagamento = id_pagamento
        self.id_pedido = id_pedido
        self.metodo = metodo
        self.valor = valor
        self.status = status
        self.chave_idempotencia = chave_idempotencia
        self.referencia_externa = referencia_externa
        self.criado_em = criado_em
        self.atualizado_em = atualizado_em
