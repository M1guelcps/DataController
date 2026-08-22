from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# Engine é o motor que gerencia a conexão com o banco
# connect_args={"check_same_thread": False} é necessário apenas para SQLite no FastAPI
engine = create_engine(
    settings.DATABASE_URL, connect_args={"check_same_thread": False}
)

# SessionLocal é a fábrica de "sessões" (transações no banco de dados)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base é a classe mãe da qual todos os nossos modelos do banco herdarão
Base = declarative_base()

# Dependência que injetaremos nas nossas rotas para pegar a conexão com o banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()