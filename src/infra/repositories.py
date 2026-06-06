from decimal import Decimal
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from src.infra.models import AccountModel, TransactionModel

class AccountRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, document_number: str) -> AccountModel:
        """Cria uma nova conta no banco de dados."""
        account = AccountModel(document_number=document_number)
        self.session.add(account)
        await self.session.commit()
        await self.session.refresh(account)
        return account

    async def get_by_id(self, account_id: int, lock_for_update: bool = False) -> Optional[AccountModel]:
        query = select(AccountModel).where(AccountModel.account_id == account_id)
        
        if lock_for_update:
            query = query.with_for_update()
            
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_document(self, document_number: str) -> Optional[AccountModel]:
        query = select(AccountModel).where(AccountModel.document_number == document_number)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_balance(self, account_id: int) -> Decimal:
        query = select(func.coalesce(func.sum(TransactionModel.amount), Decimal("0.00"))).where(
            TransactionModel.account_id == account_id
        )
        result = await self.session.execute(query)
        return Decimal(result.scalar() or "0.00")


class TransactionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, account_id: int, operation_type_id: int, amount: Decimal) -> TransactionModel:
        transaction = TransactionModel(
            account_id=account_id,
            operation_type_id=operation_type_id,
            amount=amount
        )
        self.session.add(transaction)
        await self.session.commit()
        await self.session.refresh(transaction)
        return transaction

    async def get_statement(self, account_id: int) -> List[TransactionModel]:
        query = select(TransactionModel).where(
            TransactionModel.account_id == account_id
        ).order_by(TransactionModel.event_date.desc())
        
        result = await self.session.execute(query)
        return list(result.scalars().all())