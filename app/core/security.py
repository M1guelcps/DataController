import jwt
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from core.config import settings

# Configura o passlib para usar o algoritmo bcrypt (padrão ouro para senhas)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def gerar_hash_senha(senha: str) -> str:
    return pwd_context.hash(senha)


def verificar_senha(senha_texto_puro: str, senha_hash: str) -> bool:
    return pwd_context.verify(senha_texto_puro, senha_hash)


def criar_token_jwt(dados: dict) -> str:
    dados_para_codificar = dados.copy()
    expiracao = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    dados_para_codificar.update({"exp": expiracao})

    token = jwt.encode(dados_para_codificar, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token