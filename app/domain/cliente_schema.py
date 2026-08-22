from pydantic import BaseModel

# Usado para RECEBER dados da API (POST)
class ClienteCreate(BaseModel):
    nome: str
    cnpj: str
    email: str

# Usado para DEVOLVER dados na API (Response)
class ClienteResponse(BaseModel):
    id: int
    nome: str
    cnpj: str
    email: str

    # Isso diz ao Pydantic para ler objetos do SQLAlchemy sem reclamar
    class Config:
        from_attributes = True