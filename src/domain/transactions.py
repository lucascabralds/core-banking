from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.infra.database import get_db
from src.infra.repositories import AccountRepository, TransactionRepository
from src.domain.transactions import TransactionCreate, TransactionResponse

router = APIRouter(prefix="/v1/transactions", tags=["Transações"])

@router.post("", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def create_transaction(payload: TransactionCreate, db: AsyncSession = Depends(get_db)):
    account_repo = AccountRepository(db)
    transaction_repo = TransactionRepository(db)
    
    # 1. Busca a conta aplicando o Lock Pessimista (SELECT FOR UPDATE) para evitar concorrência
    account = await account_repo.get_by_id(payload.account_id, lock_for_update=True)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conta informada não existe."
        )
        
    # 2. Calcula o valor ajustado (Débitos ficam negativos via propriedade do domínio)
    final_amount = payload.adjusted_amount
    
    # 3. Se for uma operação de débito (1, 2 ou 3), valida se há saldo suficiente
    if payload.operation_type_id in [1, 2, 3]:
        current_balance = await account_repo.get_balance(payload.account_id)
        # Como final_amount é negativo, se o saldo atual for menor que o valor absoluto do débito, barra a operação
        if current_balance < abs(final_amount):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Saldo insuficiente para realizar esta operação."
            )
            
    # 4. Registra a transação de forma imutável no Ledger
    transaction = await transaction_repo.create(
        account_id=payload.account_id,
        operation_type_id=payload.operation_type_id,
        amount=final_amount
    )
    
    return transaction