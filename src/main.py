from fastapi import FastAPI
from src.infra.database import engine, Base
from src.api.v1.accounts import router as accounts_router
from src.api.v1.transactions import router as transactions_router

app = FastAPI(
    title="Core-Banking Pro",
    description="API assíncrona de alta performance para controle de contas e transações.",
    version="1.0.0"
)

# Registra as rotas na aplicação principal
app.include_router(accounts_router)
app.include_router(transactions_router)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/health", tags=["Monitoramento"])
async def health_check():
    return {"status": "healthy", "database": "connected"}