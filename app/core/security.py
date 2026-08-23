import jwt
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from app.core.config import settings
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

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


# Diz ao FastAPI onde os usuários pegam o token (nossa rota de login)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")



# Esta função é o nosso "Segurança"
def usuario_atual(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Tenta abrir o crachá com a nossa chave secreta
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        return payload # Retorna os dados do usuário logado
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )