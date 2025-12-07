from datetime import timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ...core.config import get_settings
from ...core.security import create_access_token, get_password_hash, verify_password
from ...db.session import get_db
from ...models.app import Perfil, Usuario
from ...schemas.auth import LoginData, Token, UsuarioCreate, UsuarioOut

router = APIRouter()
settings = get_settings()


def _get_or_create_perfil(db: Session, nome: str) -> Perfil:
    perfil = db.query(Perfil).filter(Perfil.nome == nome).first()
    if not perfil:
        perfil = Perfil(nome=nome, descricao=nome)
        db.add(perfil)
        db.commit()
        db.refresh(perfil)
    return perfil


@router.post("/login", response_model=Token)
def login(data: LoginData, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.email == data.email).first()
    if not user or not verify_password(data.senha, user.senha_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(data={"sub": str(user.id)}, expires_delta=access_token_expires)
    return {"access_token": token, "token_type": "bearer"}


@router.post("/registro", response_model=UsuarioOut)
def registrar_usuario(payload: UsuarioCreate, db: Session = Depends(get_db)):
    existing = db.query(Usuario).filter(Usuario.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    perfil = _get_or_create_perfil(db, payload.perfil)
    usuario = Usuario(
        nome=payload.nome,
        email=payload.email,
        senha_hash=get_password_hash(payload.senha),
        perfil_id=perfil.id,
        id_municipio=payload.id_municipio,
        ativo=True,
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return UsuarioOut(
        id=usuario.id,
        nome=usuario.nome,
        email=usuario.email,
        perfil=perfil.nome,
        id_municipio=usuario.id_municipio,
    )
