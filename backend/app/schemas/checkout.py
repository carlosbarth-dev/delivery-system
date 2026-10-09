"""Contratos de entrada do checkout e pagamento."""

from typing import Annotated, Optional

from fastapi import Header
from pydantic import BaseModel, Field

from app.models import StatusPagamento, StatusPedido, TipoRecebimento

ChaveIdempotencia = Annotated[str, Header(alias="Idempotency-Key", min_length=8, max_length=100)]


class ItemCheckoutEntrada(BaseModel):
    produto_id: int = Field(gt=0)
    quantidade: int = Field(gt=0, le=100)


class CheckoutEntrada(BaseModel):
    cliente_id: int = Field(gt=0)
    restaurante_id: int = Field(gt=0)
    tipo_recebimento: TipoRecebimento
    itens: list[ItemCheckoutEntrada] = Field(min_length=1)


class PagamentoEntrada(BaseModel):
    pedido_id: int = Field(gt=0)
    metodo: str = Field(min_length=2, max_length=30)


class AtualizacaoPagamento(BaseModel):
    status: StatusPagamento
    referencia_externa: Optional[str] = Field(default=None, max_length=100)


class AtualizacaoPedido(BaseModel):
    status: StatusPedido
