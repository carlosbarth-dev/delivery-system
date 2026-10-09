"""Acesso ao MySQL usado pelas rotas do MVP."""

import os
from urllib.parse import unquote, urlparse

import mysql.connector


def conectar():
    """Abre uma conexão usando DATABASE_URL ou variáveis MYSQL_* do ambiente."""
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        url = urlparse(database_url)
        return mysql.connector.connect(
            host=url.hostname or "localhost",
            port=url.port or 3306,
            user=unquote(url.username or "root"),
            password=unquote(url.password or ""),
            database=(url.path or "/delivery_db").lstrip("/"),
        )
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", ""),
        database=os.getenv("MYSQL_DATABASE", "delivery_db"),
    )
