from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from domain.cliente_schema import ClienteCreate, ClienteResponse
from services.cliente_service import ClienteService
from services.excel_service import ExcelImportService
from core.security import usuario_atual

router = APIRouter(prefix="/clientes", tags=["Clientes"])

@router.post("/", response_model=ClienteResponse)
def criar_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    try:
        # Repassa o trabalho pesado para o Service
        return ClienteService.criar_cliente(db, cliente)
    except ValueError as e:
        # Se o Service reclamar (ex: CNPJ duplicado), convertemos para um Erro HTTP 400
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/importar")
async def importar_clientes_excel(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # 1. Verifica se o arquivo possui nome
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="O arquivo enviado não possui nome."
        )

    # 2. Valida a extensão
    if not file.filename.lower().endswith((".xlsx", ".xls", ".xlsb")):
        raise HTTPException(
            status_code=400,
            detail="Envie apenas arquivos .xlsx, .xlsb ou .xls"
        )

    # 3. Lê os bytes do arquivo
    conteudo = await file.read()

    try:
        # 4. Extrai os dados do Excel
        clientes_extraidos = ExcelImportService.extrair_clientes(conteudo)

        # 5. Salva no banco
        resultado = ClienteService.importar_lote(
            db,
            clientes_extraidos
        )

        return resultado

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno ao processar arquivo: {str(e)}"
        )

@router.get("/", response_model=List[ClienteResponse])
def listar_clientes(db: Session = Depends(get_db)):
    return ClienteService.listar_clientes(db)



# No APIRouter, adicionamos o dependencies=[Depends(usuario_atual)]
# Isso aplica a trava de segurança para TODAS as rotas de clientes de uma vez só!
router = APIRouter(
    prefix="/clientes",
    tags=["Clientes"],
    dependencies=[Depends(usuario_atual)]
)