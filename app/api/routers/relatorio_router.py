from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import usuario_atual
from app.services.relatorio_service import RelatorioService

# Protegemos TODA a rota de relatórios para apenas usuários logados
router = APIRouter(
    prefix="/relatorios",
    tags=["Relatórios"],
    dependencies=[Depends(usuario_atual)]
)


@router.get("/clientes/download")
def baixar_relatorio_clientes(db: Session = Depends(get_db)):
    try:
        # Chama nosso serviço que devolve o arquivo em memória
        arquivo = RelatorioService.gerar_relatorio_clientes(db)

        # Configura os cabeçalhos HTTP para forçar o navegador/app a fazer o download
        headers = {
            "Content-Disposition": 'attachment; filename="relatorio_oficial_clientes.xlsx"'
        }

        # Retorna o arquivo com o MIME Type oficial do Excel
        return StreamingResponse(
            arquivo,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers=headers
        )
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))