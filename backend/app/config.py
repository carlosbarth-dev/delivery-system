"""
Configuração Central - Backend

Carrega variáveis de ambiente e configura:
- Database (SQLAlchemy)
- Settings da aplicação
- Conexões

Veja docs/SETUP_LOCAL.md para como rodar.
"""

import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from pydantic_settings import BaseSettings


# ==========================================
# Settings (Pydantic)
# ==========================================
class Settings(BaseSettings):
    """Configurações da aplicação."""
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "sqlite:///./delivery.db"
    )
    
    # App
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-change-me")
    
    # API
    API_PORT: int = int(os.getenv("API_PORT", 8000))
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    
    # CORS
    CORS_ORIGINS: list = [
        "http://localhost:5173",  # Frontend dev
        "http://localhost:3000",  # Alternative
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Instância global de settings
settings = Settings()


# ==========================================
# SQLAlchemy Setup
# ==========================================

# Base para os models (ORM)
Base = declarative_base()

# Engine - conexão com banco de dados
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {},
    echo=settings.DEBUG  # Log de SQL em desenvolvimento
)

# Session Factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db():
    """
    Dependency injection para FastAPI.
    
    Uso em endpoints:
        @app.get("/produtos")
        def get_products(db: Session = Depends(get_db)):
            return db.query(Product).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Inicializa o banco de dados.
    
    Cria todas as tabelas baseado nos models.
    Executa seed data (produtos iniciais, etc).
    
    TODO (T0.1 - Seed):
    - Criar 3-5 produtos de exemplo (ver teste_1/app.py linha 80)
    - Inserir no banco se estiver vazio
    - Referência: docs/ARQUITETURA.md seção "Seed Data"
    """
    
    # Criar todas as tabelas baseado nos models
    Base.metadata.create_all(bind=engine)
    
    # TODO (T0.2): Implementar seed de produtos iniciais
    # db = SessionLocal()
    # if not db.query(Product).first():
    #     products = [
    #         Product(name="Neon Smash", price=29.90, description="..."),
    #         Product(name="Cyber Fries", price=16.90, description="..."),
    #         Product(name="Pink Lemonade", price=10.00, description="..."),
    #     ]
    #     db.add_all(products)
    #     db.commit()
    # db.close()
    
    print("✅ Database initialized")


# ==========================================
# Logging (v0.2.0)
# ==========================================
# TODO: Adicionar logging estruturado em v0.2.0
# import logging
# logger = logging.getLogger(__name__)
