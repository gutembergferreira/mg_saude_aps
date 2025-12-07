from typing import Optional

from pydantic import BaseModel, Field, constr


class LoginData(BaseModel):
    email: constr(min_length=3)
    senha: str = Field(alias="password")

    class Config:
        populate_by_name = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UsuarioCreate(BaseModel):
    nome: str
    email: constr(min_length=3)
    senha: str
    perfil: str = "profissional"
    id_municipio: Optional[int] = None


class UsuarioOut(BaseModel):
    id: int
    nome: str
    email: str
    perfil: str
    id_municipio: Optional[int]

    class Config:
        from_attributes = True
