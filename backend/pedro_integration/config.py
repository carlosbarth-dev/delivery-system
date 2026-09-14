"""Configuração da integração, sem credenciais dentro do repositório."""

from dataclasses import dataclass, field
import json
import os
from pathlib import Path
from urllib.parse import unquote, urlsplit

from dotenv import load_dotenv


_ENV_FILE = Path(__file__).resolve().parents[1] / ".env"


def _origens(valor: str) -> tuple[str, ...]:
    if valor.lstrip().startswith("["):
        lista = json.loads(valor)
        if not isinstance(lista, list):
            raise ValueError("CORS_ORIGINS deve conter uma lista.")
    else:
        lista = valor.split(",")

    origens = tuple(str(item).strip().rstrip("/") for item in lista)
    if not origens or any(not origem or origem == "*" for origem in origens):
        raise ValueError("Informe origens CORS explícitas; '*' não é aceito.")
    for origem in origens:
        partes = urlsplit(origem)
        if (
            partes.scheme not in {"http", "https"}
            or not partes.netloc
            or partes.path
            or partes.query
            or partes.fragment
            or partes.username
            or partes.password
        ):
            raise ValueError("Cada origem CORS deve ser somente protocolo, host e porta.")
    return origens


@dataclass(frozen=True)
class Settings:
    database_url: str = field(repr=False)
    app_env: str = "development"
    cors_origins: tuple[str, ...] = ("http://localhost:5173",)
    seed_demo: bool = True

    def __post_init__(self) -> None:
        if self.app_env not in {"development", "test", "production"}:
            raise ValueError("APP_ENV deve ser development, test ou production.")
        _origens(",".join(self.cors_origins))
        if not (
            self.database_url.startswith("sqlite:///")
            or self.database_url.startswith("mysql+mysqlconnector://")
        ):
            raise ValueError("DATABASE_URL deve usar SQLite ou mysql+mysqlconnector.")
        if self.database_url.startswith("mysql+mysqlconnector://"):
            usuario = unquote(urlsplit(self.database_url).username or "")
            if not usuario or usuario.lower() == "root":
                raise ValueError("Use um usuário próprio da aplicação, nunca root.")
        if self.app_env == "production" and self.seed_demo:
            raise ValueError("Dados de demonstração não podem ser ativados em produção.")


def load_settings() -> Settings:
    load_dotenv(_ENV_FILE, override=False)
    ambiente = os.getenv("APP_ENV", "development").strip().lower()
    if ambiente == "production" and not os.getenv("DATABASE_URL"):
        raise ValueError("DATABASE_URL é obrigatória em produção.")
    if ambiente == "production" and not os.getenv("CORS_ORIGINS"):
        raise ValueError("CORS_ORIGINS é obrigatória em produção.")

    demo_padrao = "true" if ambiente == "development" else "false"
    demo_texto = os.getenv("SEED_DEMO", demo_padrao).strip().lower()
    if demo_texto not in {"true", "false"}:
        raise ValueError("SEED_DEMO deve ser true ou false.")
    return Settings(
        database_url=os.getenv(
            "DATABASE_URL",
            "sqlite:///./backend/pedro_integration/pedro_delivery.db",
        ),
        app_env=ambiente,
        cors_origins=_origens(os.getenv("CORS_ORIGINS", "http://localhost:5173")),
        seed_demo=demo_texto == "true",
    )
