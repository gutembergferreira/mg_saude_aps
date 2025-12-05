from sqlalchemy.orm import Session

from backend.app.db.session import SessionLocal
from backend.app.models.dw import DimMunicipio

MUNICIPIOS = [
    {"codigo_ibge": "2611606", "nome": "Recife", "uf": "PE"},
    {"codigo_ibge": "1302603", "nome": "Manaus", "uf": "AM"},
    {"codigo_ibge": "3106200", "nome": "Belo Horizonte", "uf": "MG"},
]


def seed(session: Session):
    for mun in MUNICIPIOS:
        existente = session.query(DimMunicipio).filter(DimMunicipio.codigo_ibge == mun["codigo_ibge"]).first()
        if not existente:
            session.add(
                DimMunicipio(
                    codigo_ibge=mun["codigo_ibge"],
                    nome=mun["nome"],
                    uf=mun["uf"],
                )
            )
    session.commit()


if __name__ == "__main__":
    with SessionLocal() as db:
        seed(db)
        print("Seed municipios concluído.")
