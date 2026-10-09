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
from app.config import settings


def create_app() -> FastAPI:
    """
    Factory function para criar e configurar a aplicação FastAPI.
    
    Retorna:
        FastAPI: Aplicação configurada pronta para rodar
    
    Registra endpoints do fluxo de checkout e pagamento do MVP.
    """
    
    # Criar instância FastAPI
    app = FastAPI(
        title="Sistema de Delivery v0.1.0",
        description="API de delivery com checkout, pedidos e pagamentos do MVP",
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
        return {
            "status": "ok",
            "version": "0.1.0",
            "database": "ready"  # TODO: implementar check real
        }
    
    from app.routes import checkout_router
    app.include_router(checkout_router, tags=["checkout", "pedidos", "pagamentos"])
    
    return app
