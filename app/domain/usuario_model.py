from sqlalchemy import Column, Integer, String, Boolean
from app.core.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    email = Column(String, unique=True, index=True)
    senha_hash = Column(String) # NUNCA guardamos a senha em texto!
    ativo = Column(Boolean, default=True)
    perfil = Column(String, default="operador") # ex: "admin", "operador"