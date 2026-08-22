from sqlalchemy.orm import Session
from repositories.cliente_repository import ClienteRepository
from domain.cliente_schema import ClienteCreate


class ClienteService:

    @staticmethod
    def criar_cliente(db: Session, cliente: ClienteCreate):
        # 1. Regra de Negócio: Não permitir CNPJ duplicado
        cliente_existente = ClienteRepository.buscar_por_cnpj(db, cliente.cnpj)
        if cliente_existente:
            raise ValueError("Já existe um cliente cadastrado com este CNPJ.")

        # 2. Outras validações poderiam entrar aqui (ex: validar formato do CNPJ)

        # 3. Se tudo estiver certo, manda salvar
        return ClienteRepository.criar(db, cliente)

    @staticmethod
    def listar_clientes(db: Session):
        return ClienteRepository.buscar_todos(db)