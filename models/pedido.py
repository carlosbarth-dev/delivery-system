from datetime import datetime
from decimal import Decimal
from enum import Enum


class TipoRecebimento(str, Enum):
    ENTREGA = "ENTREGA"
    RETIRADA = "RETIRADA"


class StatusPedido(str, Enum):
    AGUARDANDO_PAGAMENTO = "AGUARDANDO_PAGAMENTO"
    CONFIRMADO = "CONFIRMADO"
    EM_PREPARO = "EM_PREPARO"
    PRONTO_PARA_RETIRADA = "PRONTO_PARA_RETIRADA"
    SAIU_PARA_ENTREGA = "SAIU_PARA_ENTREGA"
    ENTREGUE = "ENTREGUE"
    CANCELADO = "CANCELADO"


class Pedido:
    """Molde de domínio; os valores monetários são snapshots do checkout."""

    def __init__(
        self,
        id_pedido,
        id_cliente,
        data_pedido: datetime | None = None,
        status: StatusPedido = StatusPedido.AGUARDANDO_PAGAMENTO,
        valor_total: Decimal = Decimal("0.00"),
        id_restaurante=None,
        subtotal: Decimal = Decimal("0.00"),
        taxa_entrega: Decimal = Decimal("0.00"),
        tipo_recebimento: TipoRecebimento = TipoRecebimento.ENTREGA,
        chave_idempotencia: str | None = None,
        atualizado_em: datetime | None = None,
    ):
        self.id_pedido = id_pedido
        self.id_cliente = id_cliente
        self.id_restaurante = id_restaurante
        self.data_pedido = data_pedido
        self.status = status
        self.subtotal = subtotal
        self.taxa_entrega = taxa_entrega
        self.valor_total = valor_total
        self.tipo_recebimento = tipo_recebimento
        self.chave_idempotencia = chave_idempotencia
        self.atualizado_em = atualizado_em
