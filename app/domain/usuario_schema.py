from pydantic import BaseModel

class UsuarioCreate(BaseModel):
    nome: str
    email: str
    senha: str # Recebe a senha limpa da UI

class Token(BaseModel):
    access_token: str
    token_type: str