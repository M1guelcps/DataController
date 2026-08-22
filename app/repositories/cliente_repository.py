from sqlalchemy.orm import Session
from domain.cliente_model import Cliente
from domain.cliente_schema import ClienteCreate


class ClienteRepository:

    @staticmethod
    def buscar_por_cnpj(db: Session, cnpj: str):
        return db.query(Cliente).filter(Cliente.cnpj == cnpj).first()

    @staticmethod
    def buscar_todos(db: Session):
        return db.query(Cliente).all()

    @staticmethod
    def criar(db: Session, cliente: ClienteCreate):
        # Transforma o Schema (Pydantic) em Model (SQLAlchemy)
        db_cliente = Cliente(
            nome=cliente.nome,
            cnpj=cliente.cnpj,
            email=cliente.email
        )
        db.add(db_cliente)
        db.commit()
        db.refresh(db_cliente)  # Atualiza o objeto com o ID gerado pelo banco
        return db_cliente