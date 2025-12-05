from datetime import date, timedelta
from time import perf_counter
from typing import List, Optional

from loguru import logger
from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from ..models.dw import (
    DimEquipe,
    DimMunicipio,
    DimPaciente,
    DimTempo,
    DimUnidadeSaude,
    FatoAtendimentoAPS,
)
from ..schemas.painel_clinico import CriancaOut, GestanteOut


PRENATAL_CODES = ["PRENATAL_1", "PRENATAL_2"]
CRIANCAS_FAIXAS = {"0-1", "1-4"}


def _data_corte_12m() -> date:
    return date.today() - timedelta(days=365)


def listar_gestantes_municipio(
    db: Session, codigo_ibge: str, unidade: Optional[str], equipe: Optional[str]
) -> List[GestanteOut]:
    start = perf_counter()
    corte = _data_corte_12m()
    query = (
        db.query(
            DimPaciente.id_paciente.label("id_paciente"),
            DimPaciente.hash_identificador.label("hash_identificador"),
            DimMunicipio.nome.label("municipio"),
            DimMunicipio.codigo_ibge.label("codigo_ibge"),
            DimUnidadeSaude.nome.label("unidade"),
            DimUnidadeSaude.codigo_cnes.label("codigo_unidade"),
            DimEquipe.descricao.label("equipe"),
            DimEquipe.codigo_equipe.label("codigo_equipe"),
            DimPaciente.faixa_etaria.label("faixa_etaria"),
            func.count(FatoAtendimentoAPS.id_fato_atend).label("qtd_atendimentos_12m"),
            func.max(DimTempo.data).label("data_ultimo_atendimento"),
        )
        .join(DimMunicipio, DimMunicipio.id_municipio == FatoAtendimentoAPS.id_municipio)
        .join(DimPaciente, DimPaciente.id_paciente == FatoAtendimentoAPS.id_paciente)
        .join(DimTempo, DimTempo.id_tempo == FatoAtendimentoAPS.id_tempo)
        .outerjoin(DimUnidadeSaude, DimUnidadeSaude.id_unidade == FatoAtendimentoAPS.id_unidade)
        .outerjoin(DimEquipe, DimEquipe.id_equipe == FatoAtendimentoAPS.id_equipe)
        .filter(DimMunicipio.codigo_ibge == codigo_ibge)
        .filter(DimPaciente.sexo == "F")
        .filter(DimTempo.data >= corte)
        .filter(
            or_(
                func.lower(FatoAtendimentoAPS.tipo_atendimento).like("%gest%"),
                FatoAtendimentoAPS.codigo_proced.in_(PRENATAL_CODES),
            )
        )
    )

    if unidade:
        query = query.filter(DimUnidadeSaude.codigo_cnes == unidade)
    if equipe:
        query = query.filter(DimEquipe.codigo_equipe == equipe)

    query = query.group_by(
        DimPaciente.id_paciente,
        DimPaciente.hash_identificador,
        DimMunicipio.nome,
        DimMunicipio.codigo_ibge,
        DimUnidadeSaude.nome,
        DimUnidadeSaude.codigo_cnes,
        DimEquipe.descricao,
        DimEquipe.codigo_equipe,
        DimPaciente.faixa_etaria,
    ).order_by(DimPaciente.id_paciente)

    results = query.all()
    duration_ms = (perf_counter() - start) * 1000
    logger.info("[PERF] service=listar_gestantes municipio={} rows={} duration_ms={:.2f}", codigo_ibge, len(results), duration_ms)
    return [GestanteOut(**dict(row._mapping)) for row in results]


def listar_criancas_municipio(
    db: Session, codigo_ibge: str, unidade: Optional[str], equipe: Optional[str], faixa_etaria: Optional[str]
) -> List[CriancaOut]:
    start = perf_counter()
    corte = _data_corte_12m()
    faixas_alvo = {faixa_etaria} if faixa_etaria else CRIANCAS_FAIXAS

    query = (
        db.query(
            DimPaciente.id_paciente.label("id_paciente"),
            DimPaciente.hash_identificador.label("hash_identificador"),
            DimMunicipio.nome.label("municipio"),
            DimMunicipio.codigo_ibge.label("codigo_ibge"),
            DimUnidadeSaude.nome.label("unidade"),
            DimUnidadeSaude.codigo_cnes.label("codigo_unidade"),
            DimEquipe.descricao.label("equipe"),
            DimEquipe.codigo_equipe.label("codigo_equipe"),
            DimPaciente.faixa_etaria.label("faixa_etaria"),
            func.count(FatoAtendimentoAPS.id_fato_atend).label("qtd_atendimentos_12m"),
            func.max(DimTempo.data).label("data_ultimo_atendimento"),
        )
        .join(DimMunicipio, DimMunicipio.id_municipio == FatoAtendimentoAPS.id_municipio)
        .join(DimPaciente, DimPaciente.id_paciente == FatoAtendimentoAPS.id_paciente)
        .join(DimTempo, DimTempo.id_tempo == FatoAtendimentoAPS.id_tempo)
        .outerjoin(DimUnidadeSaude, DimUnidadeSaude.id_unidade == FatoAtendimentoAPS.id_unidade)
        .outerjoin(DimEquipe, DimEquipe.id_equipe == FatoAtendimentoAPS.id_equipe)
        .filter(DimMunicipio.codigo_ibge == codigo_ibge)
        .filter(DimTempo.data >= corte)
        .filter(DimPaciente.faixa_etaria.in_(list(faixas_alvo)))
    )

    if unidade:
        query = query.filter(DimUnidadeSaude.codigo_cnes == unidade)
    if equipe:
        query = query.filter(DimEquipe.codigo_equipe == equipe)

    query = query.group_by(
        DimPaciente.id_paciente,
        DimPaciente.hash_identificador,
        DimMunicipio.nome,
        DimMunicipio.codigo_ibge,
        DimUnidadeSaude.nome,
        DimUnidadeSaude.codigo_cnes,
        DimEquipe.descricao,
        DimEquipe.codigo_equipe,
        DimPaciente.faixa_etaria,
    ).order_by(DimPaciente.id_paciente)

    results = query.all()
    duration_ms = (perf_counter() - start) * 1000
    logger.info(
        "[PERF] service=listar_criancas municipio={} rows={} duration_ms={:.2f}",
        codigo_ibge,
        len(results),
        duration_ms,
    )
    return [CriancaOut(**dict(row._mapping)) for row in results]
