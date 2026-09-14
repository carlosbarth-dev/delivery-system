"""Catálogo compatível com as tabelas categoria e produto do Victor."""

from decimal import Decimal
import sqlite3

from sqlalchemy import Boolean, CheckConstraint, ForeignKey, Integer, Numeric, String, create_engine, event, select, text
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

from .config import Settings


class Base(DeclarativeBase):
    pass


class Categoria(Base):
    __tablename__ = "categoria"

    id_categoria: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    descricao: Mapped[str | None] = mapped_column(String(255))


class Produto(Base):
    __tablename__ = "produto"
    __table_args__ = (
        CheckConstraint("preco >= 0", name="ck_produto_preco_nao_negativo"),
    )

    id_produto: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_categoria: Mapped[int] = mapped_column(ForeignKey("categoria.id_categoria"), nullable=False)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    descricao: Mapped[str | None] = mapped_column(String(255))
    preco: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    disponivel: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)


def criar_engine(settings: Settings):
    opcoes = {"pool_pre_ping": True, "echo": False}
    if settings.database_url.startswith("sqlite:///"):
        opcoes["connect_args"] = {"check_same_thread": False}
    engine = create_engine(settings.database_url, **opcoes)
    if settings.database_url.startswith("sqlite:///"):
        @event.listens_for(engine, "connect")
        def ativar_chaves_estrangeiras(conexao_dbapi, _registro):
            if isinstance(conexao_dbapi, sqlite3.Connection):
                cursor = conexao_dbapi.cursor()
                cursor.execute("PRAGMA foreign_keys = ON")
                cursor.close()
    return engine


def preparar_catalogo(engine, settings: Settings) -> None:
    """Desenvolvimento local cria SQLite; produção e MySQL exigem schema pronto."""
    if settings.database_url.startswith("sqlite:///") and settings.app_env != "production":
        Base.metadata.create_all(engine)
        if settings.seed_demo:
            _inserir_exemplos(engine)
    else:
        # Falha cedo quando o schema do Victor ou a migração não foram aplicados.
        with engine.connect() as conexao:
            conexao.execute(
                text("SELECT id_produto, nome, descricao, preco, disponivel FROM produto LIMIT 0")
            )
            conexao.execute(text("SELECT id_categoria FROM categoria LIMIT 0"))


def _inserir_exemplos(engine) -> None:
    with Session(engine) as sessao:
        if sessao.scalar(select(Produto.id_produto).limit(1)) is not None:
            return
        categoria = sessao.scalar(select(Categoria).where(Categoria.nome == "Cardápio"))
        if categoria is None:
            categoria = Categoria(nome="Cardápio", descricao="Produtos de exemplo para desenvolvimento")
            sessao.add(categoria)
            sessao.flush()
        sessao.add_all(
            [
                Produto(
                    id_categoria=categoria.id_categoria,
                    nome="Neon Smash",
                    descricao="Hambúrguer de demonstração",
                    preco=Decimal("29.90"),
                ),
                Produto(
                    id_categoria=categoria.id_categoria,
                    nome="Cyber Fries",
                    descricao="Batatas de demonstração",
                    preco=Decimal("16.90"),
                ),
                Produto(
                    id_categoria=categoria.id_categoria,
                    nome="Pink Lemonade",
                    descricao="Bebida de demonstração",
                    preco=Decimal("10.00"),
                ),
            ]
        )
        sessao.commit()
