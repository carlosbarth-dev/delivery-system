from datetime import datetime
from decimal import Decimal
from enum import Enum


class StatusPagamento(str, Enum):
    PENDENTE = "PENDENTE"
    APROVADO = "APROVADO"
    RECUSADO = "RECUSADO"
    CANCELADO = "CANCELADO"


class Payment:
    """Representa uma tentativa de pagamento e seu identificador externo."""

    def __init__(
        self,
        id_pagamento,
        id_pedido,
        metodo,
        valor: Decimal,
        status: StatusPagamento = StatusPagamento.PENDENTE,
        chave_idempotencia: str | None = None,
        referencia_externa: str | None = None,
        criado_em: datetime | None = None,
        atualizado_em: datetime | None = None,
    ):
        self.id_pagamento = id_pagamento
        self.id_pedido = id_pedido
        self.metodo = metodo
        self.valor = valor
        self.status = status
        self.chave_idempotencia = chave_idempotencia
        self.referencia_externa = referencia_externa
        self.criado_em = criado_em
        self.atualizado_em = atualizado_em
