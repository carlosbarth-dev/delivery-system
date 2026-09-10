"""
Sistema de Delivery - Backend API
FastAPI Application Factory

Uso:
    from app import create_app
    app = create_app()

Veja docs/ARQUITETURA.md para detalhes da arquitetura.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings, init_db


def create_app() -> FastAPI:
    """
    Factory function para criar e configurar a aplicação FastAPI.
    
    Retorna:
        FastAPI: Aplicação configurada pronta para rodar
    
    TODO (T1.2): 
    - Adicionar middleware de erro global (ver docs/ARQUITETURA.md)
    - Adicionar middleware de idempotência (ver docs/ARQUITETURA.md)
    - Importar e registrar routes (app/routes/)
    """
    
    # Criar instância FastAPI
    app = FastAPI(
        title="Sistema de Delivery v0.1.0",
        description="API de delivery com catálogo e pedidos anônimos",
        version="0.1.0"
    )
    
    # Configurar CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # TODO (T1.3): Adicionar middleware de tratamento de erro
    # app.add_middleware(ErrorHandlerMiddleware)
    
    # TODO (T1.4): Adicionar middleware de idempotência
    # app.add_middleware(IdempotencyMiddleware)
    
    # Health check endpoint
    @app.get("/healthcheck", tags=["health"])
    async def healthcheck():
        """Verifica se API está operacional e BD conectado."""
        # TODO (T1.1): Verificar conexão com banco de dados
        return {
            "status": "ok",
            "version": "0.1.0",
            "database": "ready"  # TODO: implementar check real
        }
    
    # TODO (T2.1): Registrar rotas de produtos
    # from app.routes import products
    # app.include_router(products.router, prefix="/api", tags=["products"])
    
    # TODO (T2.2): Registrar rotas de pedidos
    # from app.routes import orders
    # app.include_router(orders.router, prefix="/api", tags=["orders"])
    
    # Inicializar banco de dados
    init_db()
    
    return app
