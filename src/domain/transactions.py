from decimal import Decimal
from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class TransactionCreate(BaseModel):
    account_id: int = Field(..., description="ID identificador da conta corrente")
    operation_type_id: int = Field(..., description="ID do tipo de operação (1 a 4)")
    amount: Decimal = Field(..., description="Valor nominal da transação (sempre positivo na requisição)", gt=0)

    @field_validator("operation_type_id")
    @classmethod
    def validate_operation_type(cls, value: int) -> int:
        if value not in [1, 2, 3, 4]:
            raise ValueError("Tipo de operação inválido. Valores permitidos: 1, 2, 3 ou 4.")
        return value

    @property
    def adjusted_amount(self) -> Decimal:
        """
        Regra de Ouro (Ledger): Tipos 1, 2 e 3 são débitos (devem ser armazenados como negativos).
        Tipo 4 é crédito (deve ser armazenado como positivo).
        """
        if self.operation_type_id in [1, 2, 3]:
            return -abs(self.amount)
        return abs(self.amount)



class TransactionResponse(BaseModel):
    transaction_id: int
    account_id: int
    operation_type_id: int
    amount: Decimal
    event_date: datetime

    class Config:
        from_attributes = True