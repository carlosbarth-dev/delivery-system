from decimal import Decimal
from typing import Annotated

import mysql.connector
from fastapi import FastAPI, Header, HTTPException, status
from pydantic import BaseModel, Field

from models.database.conexao import conectar
from models.pedido import StatusPedido, TipoRecebimento
from models.payment import StatusPagamento

app = FastAPI(title="API Delivery", version="1.0.0")

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
    referencia_externa: str | None = Field(default=None, max_length=100)


class AtualizacaoPedido(BaseModel):
    status: StatusPedido


def _erro(status_code: int, detail: str) -> None:
    raise HTTPException(status_code=status_code, detail=detail)


def _pedido_dict(linha: dict) -> dict:
    return {
        "id": linha["id_pedido"],
        "cliente_id": linha["id_cliente"],
        "restaurante_id": linha["id_restaurante"],
        "status": linha["status"],
        "tipo_recebimento": linha["tipo_recebimento"],
        "subtotal": float(linha["subtotal"]),
        "taxa_entrega": float(linha["taxa_entrega"]),
        "total": float(linha["valor_total"]),
        "criado_em": linha["data_pedido"],
        "atualizado_em": linha["atualizado_em"],
    }


def _pagamento_dict(linha: dict) -> dict:
    return {
        "id": linha["id_pagamento"],
        "pedido_id": linha["id_pedido"],
        "metodo": linha["metodo"],
        "valor": float(linha["valor"]),
        "status": linha["status"],
        "referencia_externa": linha["referencia_externa"],
        "criado_em": linha["criado_em"],
        "atualizado_em": linha["atualizado_em"],
    }


def _buscar_pedido(cursor, pedido_id: int) -> dict:
    cursor.execute("SELECT * FROM pedido WHERE id_pedido = %s", (pedido_id,))
    pedido = cursor.fetchone()
    if not pedido:
        _erro(status.HTTP_404_NOT_FOUND, "Pedido não encontrado.")
    return pedido


@app.get("/")
def inicio():
    return {"mensagem": "API Delivery funcionando!"}


@app.get("/health")
def health_check():
    return {"status": "online"}


@app.post("/checkout", status_code=status.HTTP_201_CREATED)
def criar_checkout(entrada: CheckoutEntrada, idempotency_key: ChaveIdempotencia):
    """Calcula valores no servidor e cria pedido e itens em uma única transação."""
    banco = conectar()
    cursor = banco.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM pedido WHERE chave_idempotencia = %s", (idempotency_key,))
        existente = cursor.fetchone()
        if existente:
            return {"pedido": _pedido_dict(existente), "reutilizado": True}

        cursor.execute("SELECT id_cliente FROM cliente WHERE id_cliente = %s", (entrada.cliente_id,))
        if not cursor.fetchone():
            _erro(status.HTTP_404_NOT_FOUND, "Cliente não encontrado.")

        cursor.execute(
            "SELECT id_restaurante, taxa_entrega FROM restaurante WHERE id_restaurante = %s AND ativo = TRUE",
            (entrada.restaurante_id,),
        )
        restaurante = cursor.fetchone()
        if not restaurante:
            _erro(status.HTTP_404_NOT_FOUND, "Restaurante não encontrado ou inativo.")

        itens_calculados: list[tuple] = []
        subtotal = Decimal("0.00")
        produtos_repetidos = set()
        for item in entrada.itens:
            if item.produto_id in produtos_repetidos:
                _erro(status.HTTP_422_UNPROCESSABLE_ENTITY, "Envie cada produto apenas uma vez.")
            produtos_repetidos.add(item.produto_id)
            cursor.execute(
                """SELECT id_produto, nome, preco FROM produto
                   WHERE id_produto = %s AND id_restaurante = %s AND disponivel = TRUE""",
                (item.produto_id, entrada.restaurante_id),
            )
            produto = cursor.fetchone()
            if not produto:
                _erro(status.HTTP_422_UNPROCESSABLE_ENTITY, f"Produto {item.produto_id} indisponível neste restaurante.")
            preco = Decimal(produto["preco"])
            subtotal += preco * item.quantidade
            itens_calculados.append((produto["id_produto"], produto["nome"], item.quantidade, preco))

        taxa_entrega = Decimal(restaurante["taxa_entrega"]) if entrada.tipo_recebimento == TipoRecebimento.ENTREGA else Decimal("0.00")
        total = subtotal + taxa_entrega
        cursor.execute(
            """INSERT INTO pedido
               (id_cliente, id_restaurante, status, tipo_recebimento, subtotal, taxa_entrega, valor_total, chave_idempotencia)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
            (entrada.cliente_id, entrada.restaurante_id, StatusPedido.AGUARDANDO_PAGAMENTO.value,
             entrada.tipo_recebimento.value, subtotal, taxa_entrega, total, idempotency_key),
        )
        pedido_id = cursor.lastrowid
        cursor.executemany(
            """INSERT INTO item_pedido (id_pedido, id_produto, nome_produto, quantidade, preco_unitario)
               VALUES (%s, %s, %s, %s, %s)""",
            [(pedido_id, *item) for item in itens_calculados],
        )
        banco.commit()
        _buscar_pedido(cursor, pedido_id)
        return {"pedido": _pedido_dict(_buscar_pedido(cursor, pedido_id)), "reutilizado": False}
    except mysql.connector.Error as erro_mysql:
        banco.rollback()
        if erro_mysql.errno == 1062:
            cursor.execute("SELECT * FROM pedido WHERE chave_idempotencia = %s", (idempotency_key,))
            existente = cursor.fetchone()
            if existente:
                return {"pedido": _pedido_dict(existente), "reutilizado": True}
        raise HTTPException(status_code=500, detail="Não foi possível criar o checkout.") from erro_mysql
    finally:
        cursor.close()
        banco.close()


@app.get("/pedidos/{pedido_id}")
def consultar_pedido(pedido_id: int):
    banco = conectar()
    cursor = banco.cursor(dictionary=True)
    try:
        pedido = _buscar_pedido(cursor, pedido_id)
        cursor.execute("SELECT id_item, id_produto, nome_produto, quantidade, preco_unitario FROM item_pedido WHERE id_pedido = %s", (pedido_id,))
        resultado = _pedido_dict(pedido)
        resultado["itens"] = [
            {**item, "preco_unitario": float(item["preco_unitario"])} for item in cursor.fetchall()
        ]
        return resultado
    finally:
        cursor.close()
        banco.close()


@app.post("/pagamentos", status_code=status.HTTP_201_CREATED)
def iniciar_pagamento(entrada: PagamentoEntrada, idempotency_key: ChaveIdempotencia):
    banco = conectar()
    cursor = banco.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM pagamento WHERE chave_idempotencia = %s", (idempotency_key,))
        existente = cursor.fetchone()
        if existente:
            return {"pagamento": _pagamento_dict(existente), "reutilizado": True}
        pedido = _buscar_pedido(cursor, entrada.pedido_id)
        if pedido["status"] == StatusPedido.CANCELADO.value:
            _erro(status.HTTP_409_CONFLICT, "Não é possível pagar um pedido cancelado.")
        cursor.execute("SELECT id_pagamento FROM pagamento WHERE id_pedido = %s AND status = 'APROVADO'", (entrada.pedido_id,))
        if cursor.fetchone():
            _erro(status.HTTP_409_CONFLICT, "Este pedido já possui pagamento aprovado.")
        cursor.execute(
            "INSERT INTO pagamento (id_pedido, metodo, valor, status, chave_idempotencia) VALUES (%s, %s, %s, %s, %s)",
            (entrada.pedido_id, entrada.metodo, pedido["valor_total"], StatusPagamento.PENDENTE.value, idempotency_key),
        )
        banco.commit()
        cursor.execute("SELECT * FROM pagamento WHERE id_pagamento = %s", (cursor.lastrowid,))
        return {"pagamento": _pagamento_dict(cursor.fetchone()), "reutilizado": False}
    except mysql.connector.Error as erro_mysql:
        banco.rollback()
        if erro_mysql.errno == 1062:
            cursor.execute("SELECT * FROM pagamento WHERE chave_idempotencia = %s", (idempotency_key,))
            existente = cursor.fetchone()
            if existente:
                return {"pagamento": _pagamento_dict(existente), "reutilizado": True}
        raise HTTPException(status_code=500, detail="Não foi possível iniciar o pagamento.") from erro_mysql
    finally:
        cursor.close()
        banco.close()


@app.patch("/pagamentos/{pagamento_id}")
def atualizar_pagamento(pagamento_id: int, entrada: AtualizacaoPagamento):
    banco = conectar()
    cursor = banco.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM pagamento WHERE id_pagamento = %s FOR UPDATE", (pagamento_id,))
        pagamento = cursor.fetchone()
        if not pagamento:
            _erro(status.HTTP_404_NOT_FOUND, "Pagamento não encontrado.")
        pedido = _buscar_pedido(cursor, pagamento["id_pedido"])
        if pedido["status"] == StatusPedido.CANCELADO.value and entrada.status == StatusPagamento.APROVADO:
            _erro(status.HTTP_409_CONFLICT, "Não é possível aprovar pagamento de pedido cancelado.")
        cursor.execute(
            "UPDATE pagamento SET status = %s, referencia_externa = COALESCE(%s, referencia_externa) WHERE id_pagamento = %s",
            (entrada.status.value, entrada.referencia_externa, pagamento_id),
        )
        if entrada.status == StatusPagamento.APROVADO:
            cursor.execute("UPDATE pedido SET status = %s WHERE id_pedido = %s AND status = %s", (StatusPedido.CONFIRMADO.value, pagamento["id_pedido"], StatusPedido.AGUARDANDO_PAGAMENTO.value))
        banco.commit()
        cursor.execute("SELECT * FROM pagamento WHERE id_pagamento = %s", (pagamento_id,))
        return _pagamento_dict(cursor.fetchone())
    except mysql.connector.Error as erro_mysql:
        banco.rollback()
        raise HTTPException(status_code=500, detail="Não foi possível atualizar o pagamento.") from erro_mysql
    finally:
        cursor.close()
        banco.close()


@app.patch("/pedidos/{pedido_id}/status")
def atualizar_status_pedido(pedido_id: int, entrada: AtualizacaoPedido):
    transicoes = {
        StatusPedido.AGUARDANDO_PAGAMENTO.value: {StatusPedido.CANCELADO.value},
        StatusPedido.CONFIRMADO.value: {StatusPedido.EM_PREPARO.value, StatusPedido.CANCELADO.value},
        StatusPedido.EM_PREPARO.value: {StatusPedido.PRONTO_PARA_RETIRADA.value, StatusPedido.SAIU_PARA_ENTREGA.value, StatusPedido.CANCELADO.value},
        StatusPedido.PRONTO_PARA_RETIRADA.value: {StatusPedido.ENTREGUE.value, StatusPedido.CANCELADO.value},
        StatusPedido.SAIU_PARA_ENTREGA.value: {StatusPedido.ENTREGUE.value},
    }
    banco = conectar()
    cursor = banco.cursor(dictionary=True)
    try:
        pedido = _buscar_pedido(cursor, pedido_id)
        if entrada.status.value not in transicoes.get(pedido["status"], set()):
            _erro(status.HTTP_409_CONFLICT, "Transição de status inválida para este pedido.")
        if entrada.status == StatusPedido.SAIU_PARA_ENTREGA and pedido["tipo_recebimento"] != TipoRecebimento.ENTREGA.value:
            _erro(status.HTTP_422_UNPROCESSABLE_ENTITY, "Pedido de retirada não pode sair para entrega.")
        if entrada.status == StatusPedido.PRONTO_PARA_RETIRADA and pedido["tipo_recebimento"] != TipoRecebimento.RETIRADA.value:
            _erro(status.HTTP_422_UNPROCESSABLE_ENTITY, "Use 'SAIU_PARA_ENTREGA' para pedidos de entrega.")
        cursor.execute("UPDATE pedido SET status = %s WHERE id_pedido = %s", (entrada.status.value, pedido_id))
        banco.commit()
        return _pedido_dict(_buscar_pedido(cursor, pedido_id))
    finally:
        cursor.close()
        banco.close()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("models.database.api.main:app", host="127.0.0.1", port=8001, reload=True)
