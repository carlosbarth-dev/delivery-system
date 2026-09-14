"""API mínima para conectar o catálogo existente ao front."""

from contextlib import asynccontextmanager
from decimal import Decimal
import logging

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import select, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from .config import Settings, load_settings
from .database import Produto, criar_engine, preparar_catalogo


log = logging.getLogger(__name__)


class ProdutoPublico(BaseModel):
    id: int
    name: str
    price: Decimal
    description: str


class ListaProdutos(BaseModel):
    items: list[ProdutoPublico]


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or load_settings()
    engine = criar_engine(settings)

    @asynccontextmanager
    async def lifespan(_app: FastAPI):
        preparar_catalogo(engine, settings)
        try:
            yield
        finally:
            engine.dispose()

    app = FastAPI(title="Catálogo Delivery", version="0.2.0", debug=False, lifespan=lifespan)
    app.state.engine = engine
    app.add_middleware(
        CORSMiddleware,
        allow_origins=list(settings.cors_origins),
        allow_credentials=False,
        allow_methods=["GET"],
        allow_headers=["Accept", "Content-Type"],
    )

    @app.exception_handler(SQLAlchemyError)
    async def erro_banco(_request, erro: SQLAlchemyError):
        log.error("Falha de banco: %s", type(erro).__name__)
        return JSONResponse(status_code=503, content={"detail": "Banco indisponível."})

    @app.exception_handler(Exception)
    async def erro_inesperado(_request, erro: Exception):
        log.error("Falha interna: %s", type(erro).__name__)
        return JSONResponse(status_code=500, content={"detail": "Erro interno."})

    @app.get("/healthcheck")
    def healthcheck():
        with engine.connect() as conexao:
            conexao.execute(text("SELECT 1"))
            conexao.execute(select(Produto.id_produto, Produto.descricao).limit(0))
        return {"status": "ok", "database": "ready"}

    @app.get("/produtos", response_model=ListaProdutos)
    def listar_produtos(limit: int = Query(default=100, ge=1, le=100)):
        with Session(engine) as sessao:
            produtos = sessao.scalars(
                select(Produto)
                .where(Produto.disponivel.is_(True))
                .order_by(Produto.id_produto)
                .limit(limit)
            ).all()
            return {
                "items": [
                    ProdutoPublico(
                        id=produto.id_produto,
                        name=produto.nome,
                        price=produto.preco,
                        description=produto.descricao or "",
                    )
                    for produto in produtos
                ]
            }

    return app


app = create_app()
