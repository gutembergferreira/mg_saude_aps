from sqlalchemy.orm import Session

from backend.app.db.session import SessionLocal
from backend.app.models.dw import DimIndicador

INDICADORES = [
    ("C1", "Proporção de gestantes com ≥6 consultas de pré-natal"),
    ("C2", "Cobertura vacinal DTP"),
    ("C3", "Cobertura vacinal Polio"),
    ("C4", "Hipertensos acompanhados"),
    ("C5", "Diabéticos acompanhados"),
    ("C6", "Pré-natal adequado"),
    ("C7", "Saúde da criança (0-1)"),
]


def seed(session: Session):
    for codigo, nome in INDICADORES:
        existente = session.query(DimIndicador).filter(DimIndicador.codigo == codigo).first()
        if not existente:
            session.add(
                DimIndicador(
                    codigo=codigo,
                    nome=nome,
                    descricao=nome,
                    tipo="desempenho",
                    fonte_metodologia="Portaria GM/MS 3.493/2024",
                )
            )
    session.commit()


if __name__ == "__main__":
    with SessionLocal() as db:
        seed(db)
        print("Seed indicadores concluído.")
