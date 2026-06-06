from pydantic import BaseModel, Field, field_validator

class AccountCreate(BaseModel):
    document_number: str = Field(
        ..., 
        description="Número do documento único do cliente (CPF ou CNPJ)",
        min_length=11,
        max_length=14
    )

    @field_validator("document_number")
    @classmethod
    def validate_document_format(cls, value: str) -> str:
        
        cleaned = "".join(filter(str.isdigit, value))
        
        if len(cleaned) not in [11, 14]:
            raise ValueError("O documento deve ter 11 dígitos (CPF) ou 14 dígitos (CNPJ).")
            
        return cleaned

class AccountResponse(BaseModel):
    account_id: int
    document_number: str
    class Config:
        from_attributes = True  