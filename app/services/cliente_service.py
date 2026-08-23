from typing import Any

from sqlalchemy.orm import Session
from app.repositories.cliente_repository import ClienteRepository
from app.domain.cliente_schema import ClienteCreate


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


    @staticmethod
    def importar_lote(db: Session, clientes: list[ClienteCreate]):
        resultado:dict[str,Any] = {"sucessos": 0, "erros": []}

        for cliente in clientes:
            try:
                # Reutilizamos a lógica de criação que já tem a validação de CNPJ!
                ClienteService.criar_cliente(db, cliente)
                resultado["sucessos"] += 1
            except ValueError as e:
                # Se o CNPJ já existir, não quebramos tudo, apenas anotamos o erro
                resultado["erros"].append({"cnpj": cliente.cnpj, "motivo": str(e)})

        return resultado