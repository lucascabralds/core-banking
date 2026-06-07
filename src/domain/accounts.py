from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.infra.database import get_db
from src.infra.repositories import AccountRepository
from src.domain.accounts import AccountCreate, AccountResponse

router = APIRouter(prefix="/v1/accounts", tags=["Contas"])

@router.post("", response_model=AccountResponse, status_code=status.HTTP_201_CREATED)
async def create_account(payload: AccountCreate, db: AsyncSession = Depends(get_db)):
    repository = AccountRepository(db)
    
    # Valida se o documento já está cadastrado para evitar duplicidade (Regra do User_History)
    existing_account = await repository.get_by_document(payload.document_number)
    if existing_account:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Uma conta com este número de documento já existe."
        )
        
    account = await repository.create(document_number=payload.document_number)
    return account

@router.get("/{account_id}", response_model=AccountResponse)
async def get_account(account_id: int, db: AsyncSession = Depends(get_db)):
    repository = AccountRepository(db)
    
    account = await repository.get_by_id(account_id)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conta não encontrada."
        )
        
    return account