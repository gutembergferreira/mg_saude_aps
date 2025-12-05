from sqlalchemy.orm import Session

from backend.app.core.security import get_password_hash
from backend.app.db.session import SessionLocal
from backend.app.models.app import Perfil, Usuario
from backend.app.models.dw import DimMunicipio

DEFAULT_USERS = [
    {
        "nome": "Administrador",
        "email": "admin@mgsaude.local",
        "perfil": "admin",
        "senha": "Senha123!",
        "id_municipio": None,
    },
    {
        "nome": "Gestor Recife",
        "email": "gestor.recife@mgsaude.local",
        "perfil": "gestor_municipal",
        "senha": "Senha123!",
        "codigo_ibge": "2611606",
    },
    {
        "nome": "Profissional Recife",
        "email": "profissional.recife@mgsaude.local",
        "perfil": "profissional",
        "senha": "Senha123!",
        "codigo_ibge": "2611606",
    },
]


def _get_or_create_perfil(session: Session, nome: str) -> Perfil:
    perfil = session.query(Perfil).filter(Perfil.nome == nome).first()
    if not perfil:
        perfil = Perfil(nome=nome, descricao=nome)
        session.add(perfil)
        session.commit()
        session.refresh(perfil)
    return perfil


def _get_id_municipio(session: Session, codigo_ibge: str):
    mun = session.query(DimMunicipio).filter(DimMunicipio.codigo_ibge == codigo_ibge).first()
    return mun.id_municipio if mun else None


def seed(session: Session):
    for item in DEFAULT_USERS:
        perfil = _get_or_create_perfil(session, item["perfil"])
        id_municipio = item.get("id_municipio")
        if "codigo_ibge" in item:
            id_municipio = _get_id_municipio(session, item["codigo_ibge"])

        existing = session.query(Usuario).filter(Usuario.email == item["email"]).first()
        if existing:
            continue

        session.add(
            Usuario(
                nome=item["nome"],
                email=item["email"],
                senha_hash=get_password_hash(item["senha"]),
                perfil_id=perfil.id,
                id_municipio=id_municipio,
                ativo=True,
            )
        )
    session.commit()


if __name__ == "__main__":
    with SessionLocal() as db:
        seed(db)
        print("Seed usuarios concluído.")
