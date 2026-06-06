from fastapi import FastAPI
from src.infra.database import engine, Base

app = FastAPI(
    title="Pismo Core-Banking Pro",
    description="API assíncrona de alta performance para controle de contas e transações.",
    version="1.0.0"
)

# Evento do FastAPI para criar as tabelas no PostgreSQL assim que o app iniciar
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        # Cria as tabelas na base de dados caso elas não existam
        await conn.run_sync(Base.metadata.create_all)

@app.get("/health", tags=["Monitoramento"])
async def health_check():
    return {"status": "healthy", "database": "connected"}