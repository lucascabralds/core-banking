import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

# No futuro, moveremos isso para um arquivo de configuração (.env)
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql+asyncpg://pismo_user:pismo_password@localhost:5432/core_banking_prod"
)

# Cria o motor assíncrono para o PostgreSQL
engine = create_async_engine(DATABASE_URL, echo=True)

# Cria a fábrica de sessões assíncronas para as rotas da API
AsyncSessionLocal = async_sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# Classe base que todos os modelos de tabela irão herdar
Base = declarative_base()

# Função utilitária (Dependency Injection) para usar nas rotas do FastAPI
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()