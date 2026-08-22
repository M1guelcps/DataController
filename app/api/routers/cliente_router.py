from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from core.database import get_db
from domain.cliente_schema import ClienteCreate, ClienteResponse
from services.cliente_service import ClienteService

router = APIRouter(prefix="/clientes", tags=["Clientes"])

@router.post("/", response_model=ClienteResponse)
def criar_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    try:
        # Repassa o trabalho pesado para o Service
        return ClienteService.criar_cliente(db, cliente)
    except ValueError as e:
        # Se o Service reclamar (ex: CNPJ duplicado), convertemos para um Erro HTTP 400
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[ClienteResponse])
def listar_clientes(db: Session = Depends(get_db)):
    return ClienteService.listar_clientes(db)