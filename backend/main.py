"""
Entry Point - Sistema de Delivery Backend

Executa com:
    uvicorn main:app --reload

Ou se preferir via Python:
    python main.py

Documentação automática:
    http://localhost:8000/docs (Swagger UI)
    http://localhost:8000/redoc (ReDoc)

Veja docs/SETUP_LOCAL.md para mais detalhes.
"""

import uvicorn
from app import create_app

# Criar aplicação
app = create_app()


if __name__ == "__main__":
    # Executar servidor de desenvolvimento
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload em desenvolvimento
        log_level="info"
    )
