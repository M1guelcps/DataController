from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import verificar_senha, gerar_hash_senha, criar_token_jwt
from domain.usuario_schema import Token, UsuarioCreate
from domain.usuario_model import Usuario
from repositories.usuario_repository import UsuarioRepository

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post("/registrar")
def registrar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    if UsuarioRepository.buscar_por_email(db, usuario.email):
        raise HTTPException(status_code=400, detail="Email já cadastrado.")

    # Converte o Schema para Model, trocando a senha pelo Hash!
    novo_usuario = Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha_hash=gerar_hash_senha(usuario.senha)
    )
    UsuarioRepository.criar(db, novo_usuario)
    return {"mensagem": "Usuário criado com sucesso!"}


@router.post("/login", response_model=Token)
# O OAuth2PasswordRequestForm é um padrão do FastAPI que faz o Swagger habilitar o botão verde "Authorize"
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Busca o usuário no banco
    usuario = UsuarioRepository.buscar_por_email(db,
                                                 form_data.username)  # OAuth2 usa 'username' para o campo principal (nosso email)

    # Valida usuário e senha
    if not usuario or not verificar_senha(form_data.password, usuario.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Gera o crachá digital (Token)
    token = criar_token_jwt({"sub": usuario.email, "perfil": usuario.perfil})
    return {"access_token": token, "token_type": "bearer"}