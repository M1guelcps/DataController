from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "CDATA"
    VERSION: str = "0.1.0"

    # URL do banco de dados (Usando SQLite para facilitar o início)
    # Quando formos para produção, basta trocar essa string (via variável de ambiente)
    DATABASE_URL: str = "sqlite:///./banco_dados.db"

    class Config:
        case_sensitive = True


settings = Settings()