from fastapi import FastAPI
from core.config import settings
from core.database import Base, engine
from api.routers import cliente_router

# Cria as tabelas no banco de dados caso não existam
Base.metadata.create_all(bind=engine)

# Inicializa o aplicativo FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION
)

app.include_router(cliente_router.router)
# Rota básica de verificação de saúde (Health Check)
@app.get("/")
def health_check():
    return {
        "status": "online",
        "sistema": settings.PROJECT_NAME,
        "versao": settings.VERSION
    }