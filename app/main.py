from fastapi import FastAPI
from app.core.config import settings
from app.core.database import Base, engine

# Cria as tabelas no banco de dados caso não existam
Base.metadata.create_all(bind=engine)

# Inicializa o aplicativo FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION
)

# Rota básica de verificação de saúde (Health Check)
@app.get("/")
def health_check():
    return {
        "status": "online",
        "sistema": settings.PROJECT_NAME,
        "versao": settings.VERSION
    }