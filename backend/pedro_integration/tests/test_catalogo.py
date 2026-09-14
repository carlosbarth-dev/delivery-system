from decimal import Decimal

from fastapi.testclient import TestClient
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from pedro_integration.api import create_app
from pedro_integration.config import Settings, _origens
from pedro_integration.database import Categoria, Produto


def _app_temporario(tmp_path):
    arquivo = (tmp_path / "delivery.db").as_posix()
    return create_app(
        Settings(
            database_url=f"sqlite:///{arquivo}",
            app_env="test",
            cors_origins=("http://localhost:5173",),
            seed_demo=True,
        )
    )


def test_catalogo_vem_do_banco_e_obedece_contrato_do_front(tmp_path):
    app = _app_temporario(tmp_path)
    with TestClient(app) as client:
        resposta = client.get("/produtos")
        assert resposta.status_code == 200
        itens = resposta.json()["items"]
        assert len(itens) == 3
        assert set(itens[0]) == {"id", "name", "price", "description"}
        assert itens[0]["name"] == "Neon Smash"
        assert Decimal(str(itens[0]["price"])) == Decimal("29.90")
        assert client.get("/produtos").json() == resposta.json()
        assert len(client.get("/produtos?limit=1").json()["items"]) == 1


def test_produtos_indisponiveis_nao_aparecem(tmp_path):
    app = _app_temporario(tmp_path)
    with TestClient(app) as client:
        with Session(app.state.engine) as sessao:
            produto = sessao.scalar(select(Produto).where(Produto.nome == "Cyber Fries"))
            produto.disponivel = False
            sessao.commit()
        nomes = [item["name"] for item in client.get("/produtos").json()["items"]]
        assert "Cyber Fries" not in nomes


def test_validacao_bloqueia_limite_invalido_e_tentativa_de_injecao(tmp_path):
    app = _app_temporario(tmp_path)
    with TestClient(app) as client:
        for consulta in ("limit=0", "limit=101", "limit=1%3BDELETE%20FROM%20produto"):
            assert client.get(f"/produtos?{consulta}").status_code == 422
        assert len(client.get("/produtos").json()["items"]) == 3


def test_cors_so_permite_o_front_configurado(tmp_path):
    app = _app_temporario(tmp_path)
    with TestClient(app) as client:
        permitido = client.options(
            "/produtos",
            headers={
                "Origin": "http://localhost:5173",
                "Access-Control-Request-Method": "GET",
            },
        )
        assert permitido.status_code == 200
        assert permitido.headers["access-control-allow-origin"] == "http://localhost:5173"
        bloqueado = client.options(
            "/produtos",
            headers={
                "Origin": "https://site-desconhecido.example",
                "Access-Control-Request-Method": "GET",
            },
        )
        assert bloqueado.status_code == 400
        assert "access-control-allow-origin" not in bloqueado.headers


def test_healthcheck_verifica_schema_e_erro_nao_expoe_sql(tmp_path):
    app = _app_temporario(tmp_path)
    with TestClient(app, raise_server_exceptions=False) as client:
        assert client.get("/healthcheck").json()["database"] == "ready"
        with app.state.engine.begin() as conexao:
            conexao.execute(text("DROP TABLE produto"))
        resposta = client.get("/healthcheck")
        assert resposta.status_code == 503
        assert resposta.json() == {"detail": "Banco indisponível."}
        assert "SELECT" not in resposta.text


def test_preco_negativo_rejeitado_pelo_banco(tmp_path):
    app = _app_temporario(tmp_path)
    with TestClient(app):
        with Session(app.state.engine) as sessao:
            categoria = sessao.scalar(select(Categoria))
            sessao.add(
                Produto(
                    id_categoria=categoria.id_categoria,
                    nome="Inválido",
                    preco=Decimal("-1.00"),
                )
            )
            try:
                sessao.commit()
            except IntegrityError:
                sessao.rollback()
            else:
                raise AssertionError("Preço negativo não foi bloqueado.")


def test_produto_sem_categoria_rejeitado_pelo_banco(tmp_path):
    app = _app_temporario(tmp_path)
    with TestClient(app):
        with Session(app.state.engine) as sessao:
            sessao.add(
                Produto(
                    id_categoria=999999,
                    nome="Sem categoria",
                    preco=Decimal("1.00"),
                )
            )
            try:
                sessao.commit()
            except IntegrityError:
                sessao.rollback()
            else:
                raise AssertionError("Chave estrangeira inválida não foi bloqueada.")


def test_rotas_de_pagamento_nao_sao_expostas(tmp_path):
    app = _app_temporario(tmp_path)
    with TestClient(app) as client:
        assert client.post("/pagamentos").status_code == 404
        assert client.patch("/pagamentos/1").status_code == 404
        assert client.patch("/pedidos/1/status").status_code == 404


def test_configuracao_rejeita_root_e_cors_aberto():
    for usuario in ("root", "ROOT", "r%6Fot"):
        try:
            Settings(database_url=f"mysql+mysqlconnector://{usuario}:segredo@localhost/delivery")
        except ValueError:
            pass
        else:
            raise AssertionError("Usuário root foi aceito.")

    try:
        _origens("*")
    except ValueError:
        pass
    else:
        raise AssertionError("CORS aberto foi aceito.")
