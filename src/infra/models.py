import datetime
from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from src.infra.database import Base

class AccountModel(Base):
    __tablename__ = "accounts"

    account_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    # index=True e unique=True garante buscas rápidas e impede duplicidade de CPFs
    document_number = Column(String(20), unique=True, index=True, nullable=False)
    
    # Relacionamento de volta para as transações
    transactions = relationship("TransactionModel", back_populates="account")


class TransactionModel(Base):
    __tablename__ = "transactions"

    transaction_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey("accounts.account_id"), nullable=False)
    operation_type_id = Column(Integer, nullable=False)
    
    # Numeric(10, 2) suporta valores como 99.999.999,99 sem erros de arredondamento de floats
    amount = Column(Numeric(10, 2), nullable=False)
    event_date = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))

    # Relacionamento com a tabela de contas
    account = relationship("AccountModel", back_populates="transactions")