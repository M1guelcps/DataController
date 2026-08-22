from sqlalchemy.orm import Session
from domain.usuario_model import Usuario


class UsuarioRepository:

    @staticmethod
    def buscar_por_email(db: Session, email: str):
        return db.query(Usuario).filter(Usuario.email == email).first()

    @staticmethod
    def criar(db: Session, usuario_db: Usuario):
        db.add(usuario_db)
        db.commit()
        db.refresh(usuario_db)
        return usuario_db