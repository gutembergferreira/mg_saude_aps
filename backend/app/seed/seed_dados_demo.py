from datetime import date

from sqlalchemy.orm import Session

from backend.app.db.session import SessionLocal
from backend.app.models.dw import (
    DimEquipe,
    DimPaciente,
    DimTempo,
    DimTerritorio,
    DimUnidadeSaude,
    FatoAtendimentoAPS,
    FatoCadastroAPS,
    FatoIndicadorAPS,
)


def _ensure_tempo(session: Session, data_ref: date) -> int:
    tempo = session.query(DimTempo).filter(DimTempo.data == data_ref).first()
    if tempo:
        return tempo.id_tempo
    tempo = DimTempo(
        data=data_ref,
        ano=data_ref.year,
        mes=data_ref.month,
        dia=data_ref.day,
        trimestre=(data_ref.month - 1) // 3 + 1,
        quadrimestre=(data_ref.month - 1) // 4 + 1,
        nome_mes=data_ref.strftime("%B"),
        nome_dia_semana=data_ref.strftime("%A"),
        eh_final_semana=data_ref.weekday() >= 5,
    )
    session.add(tempo)
    session.commit()
    session.refresh(tempo)
    return tempo.id_tempo


def _ensure_unidade(session: Session, codigo_cnes: str, id_municipio: int) -> int:
    unidade = (
        session.query(DimUnidadeSaude)
        .filter(DimUnidadeSaude.codigo_cnes == codigo_cnes, DimUnidadeSaude.id_municipio == id_municipio)
        .first()
    )
    if unidade:
        return unidade.id_unidade
    unidade = DimUnidadeSaude(codigo_cnes=codigo_cnes, nome=f"USF {codigo_cnes}", id_municipio=id_municipio)
    session.add(unidade)
    session.commit()
    session.refresh(unidade)
    return unidade.id_unidade


def _ensure_equipe(session: Session, codigo_equipe: str, id_unidade: int) -> int:
    equipe = (
        session.query(DimEquipe)
        .filter(DimEquipe.codigo_equipe == codigo_equipe, DimEquipe.id_unidade == id_unidade)
        .first()
    )
    if equipe:
        return equipe.id_equipe
    equipe = DimEquipe(codigo_equipe=codigo_equipe, descricao=f"Equipe {codigo_equipe}", id_unidade=id_unidade)
    session.add(equipe)
    session.commit()
    session.refresh(equipe)
    return equipe.id_equipe


def _ensure_territorio(session: Session, codigo: str, id_equipe: int) -> int:
    terr = (
        session.query(DimTerritorio)
        .filter(DimTerritorio.codigo_territorio == codigo, DimTerritorio.id_equipe == id_equipe)
        .first()
    )
    if terr:
        return terr.id_territorio
    terr = DimTerritorio(codigo_territorio=codigo, descricao=f"Território {codigo}", id_equipe=id_equipe)
    session.add(terr)
    session.commit()
    session.refresh(terr)
    return terr.id_territorio


def seed(session: Session):
    # Assumindo Recife já seedado e indicadores C1-C3
    id_municipio = 1  # Recife inserido primeiro na lista de seed_municipios

    id_unidade = _ensure_unidade(session, "1234567", id_municipio)
    id_equipe = _ensure_equipe(session, "E001", id_unidade)
    id_territorio = _ensure_territorio(session, "T001", id_equipe)

    paciente1 = DimPaciente(id_municipio=id_municipio, sexo="F", faixa_etaria="20-24", hash_identificador="hash_p1")
    paciente2 = DimPaciente(id_municipio=id_municipio, sexo="M", faixa_etaria="0-1", hash_identificador="hash_p2")
    session.add_all([paciente1, paciente2])
    session.commit()
    session.refresh(paciente1)
    session.refresh(paciente2)

    data1 = date(2025, 1, 15)
    data2 = date(2025, 2, 20)
    id_t1 = _ensure_tempo(session, data1)
    id_t2 = _ensure_tempo(session, data2)

    cad1 = FatoCadastroAPS(
        id_tempo=id_t1,
        id_municipio=id_municipio,
        id_unidade=id_unidade,
        id_equipe=id_equipe,
        id_paciente=paciente1.id_paciente,
        cadastro_valido=True,
        eh_publico_alvo=True,
        peso_capitacao=1,
    )
    cad2 = FatoCadastroAPS(
        id_tempo=id_t2,
        id_municipio=id_municipio,
        id_unidade=id_unidade,
        id_equipe=id_equipe,
        id_paciente=paciente2.id_paciente,
        cadastro_valido=True,
        eh_publico_alvo=True,
        peso_capitacao=1,
    )
    session.add_all([cad1, cad2])

    at1 = FatoAtendimentoAPS(
        id_tempo=id_t1,
        id_municipio=id_municipio,
        id_unidade=id_unidade,
        id_equipe=id_equipe,
        id_paciente=paciente1.id_paciente,
        id_territorio=id_territorio,
        tipo_atendimento="Consulta gestante",
        quantidade=1,
    )
    at2 = FatoAtendimentoAPS(
        id_tempo=id_t2,
        id_municipio=id_municipio,
        id_unidade=id_unidade,
        id_equipe=id_equipe,
        id_paciente=paciente2.id_paciente,
        id_territorio=id_territorio,
        tipo_atendimento="Consulta puericultura",
        quantidade=1,
    )
    session.add_all([at1, at2])

    indic_periodos = [("2025Q1", id_t1), ("2025Q2", id_t2)]
    for periodo, id_tempo in indic_periodos:
        session.add(
            FatoIndicadorAPS(
                id_tempo=id_tempo,
                id_municipio=id_municipio,
                id_unidade=id_unidade,
                id_territorio=id_territorio,
                id_indicador=1,  # C1
                periodo_referencia=periodo,
                valor=0.85,
                meta=0.8,
                atingiu_meta=True,
            )
        )
        session.add(
            FatoIndicadorAPS(
                id_tempo=id_tempo,
                id_municipio=id_municipio,
                id_unidade=id_unidade,
                id_territorio=id_territorio,
                id_indicador=2,  # C2
                periodo_referencia=periodo,
                valor=0.75,
                meta=0.8,
                atingiu_meta=False,
            )
        )
    session.commit()


if __name__ == "__main__":
    with SessionLocal() as db:
        seed(db)
        print("Seed dados demo concluído.")
