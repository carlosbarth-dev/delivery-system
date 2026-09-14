"""Verificação opcional, somente de leitura, para o banco MySQL do grupo."""

import os

import pytest
from fastapi.testclient import TestClient

from pedro_integration.api import create_app
from pedro_integration.config import Settings


def test_mysql_real_quando_configurado():
    url = os.getenv("TEST_MYSQL_URL")
    if not url:
        pytest.skip("Defina TEST_MYSQL_URL para testar o MySQL do grupo.")
    if not url.startswith("mysql+mysqlconnector://"):
        pytest.fail("TEST_MYSQL_URL precisa apontar para MySQL.")

    app = create_app(
        Settings(
            database_url=url,
            app_env="test",
            cors_origins=("http://localhost:5173",),
            seed_demo=False,
        )
    )
    with TestClient(app) as client:
        assert client.get("/healthcheck").status_code == 200
        resposta = client.get("/produtos")
        assert resposta.status_code == 200
        assert "items" in resposta.json()
