from datetime import date, timedelta
from time import perf_counter
from typing import List

from loguru import logger
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..models.dw import (
    DimIndicador,
    DimMunicipio,
    DimTerritorio,
    DimTempo,
    DimUnidadeSaude,
    FatoAtendimentoAPS,
    FatoCadastroAPS,
    FatoIndicadorAPS,
)
from ..schemas.geoprocessamento import (
    IndicadorTerritorioGeoOut,
    IndicadorUnidadeGeoOut,
    UnidadeGeoOut,
)


def _corte_12m() -> date:
    return date.today() - timedelta(days=365)


def listar_unidades_geo(db: Session, codigo_ibge: str) -> List[UnidadeGeoOut]:
    start = perf_counter()
    corte = _corte_12m()
    sub_cad = (
        db.query(
            FatoCadastroAPS.id_unidade.label("id_unidade"),
            func.count(FatoCadastroAPS.id_fato_cad).label("qtd_cadastros"),
        )
        .join(DimMunicipio, DimMunicipio.id_municipio == FatoCadastroAPS.id_municipio)
        .filter(DimMunicipio.codigo_ibge == codigo_ibge)
        .group_by(FatoCadastroAPS.id_unidade)
        .subquery()
    )

    sub_atend = (
        db.query(
            FatoAtendimentoAPS.id_unidade.label("id_unidade"),
            func.count(FatoAtendimentoAPS.id_fato_atend).label("qtd_atendimentos"),
        )
        .join(DimMunicipio, DimMunicipio.id_municipio == FatoAtendimentoAPS.id_municipio)
        .join(DimTempo, DimTempo.id_tempo == FatoAtendimentoAPS.id_tempo)
        .filter(DimMunicipio.codigo_ibge == codigo_ibge)
        .filter(DimTempo.data >= corte)
        .filter(FatoAtendimentoAPS.id_unidade.isnot(None))
        .group_by(FatoAtendimentoAPS.id_unidade)
        .subquery()
    )

    query = (
        db.query(
            DimUnidadeSaude.id_unidade.label("id_unidade"),
            DimUnidadeSaude.codigo_cnes.label("codigo_cnes"),
            DimUnidadeSaude.nome.label("nome"),
            DimUnidadeSaude.latitude.label("latitude"),
            DimUnidadeSaude.longitude.label("longitude"),
            func.coalesce(sub_cad.c.qtd_cadastros, 0).label("quantidade_cadastros"),
            func.coalesce(sub_atend.c.qtd_atendimentos, 0).label("quantidade_atendimentos_12m"),
        )
        .join(DimMunicipio, DimMunicipio.id_municipio == DimUnidadeSaude.id_municipio)
        .filter(DimMunicipio.codigo_ibge == codigo_ibge)
        .outerjoin(sub_cad, sub_cad.c.id_unidade == DimUnidadeSaude.id_unidade)
        .outerjoin(sub_atend, sub_atend.c.id_unidade == DimUnidadeSaude.id_unidade)
        .order_by(DimUnidadeSaude.id_unidade)
    )

    results = query.all()
    duration_ms = (perf_counter() - start) * 1000
    logger.info("[PERF] service=listar_unidades_geo municipio={} rows={} duration_ms={:.2f}", codigo_ibge, len(results), duration_ms)
    return [UnidadeGeoOut(**dict(row._mapping)) for row in results]


def listar_indicador_geo_unidade(
    db: Session, codigo_ibge: str, indicador: str, periodo: str
) -> List[IndicadorUnidadeGeoOut]:
    start = perf_counter()
    query = (
        db.query(
            DimUnidadeSaude.id_unidade.label("id_unidade"),
            DimUnidadeSaude.codigo_cnes.label("codigo_cnes"),
            DimUnidadeSaude.nome.label("nome"),
            DimUnidadeSaude.latitude.label("latitude"),
            DimUnidadeSaude.longitude.label("longitude"),
            func.avg(FatoIndicadorAPS.valor).label("valor_indicador"),
            func.avg(FatoIndicadorAPS.meta).label("meta"),
            func.max(func.coalesce(FatoIndicadorAPS.atingiu_meta, False)).label("atingiu_meta"),
        )
        .join(DimMunicipio, DimMunicipio.id_municipio == FatoIndicadorAPS.id_municipio)
        .join(DimUnidadeSaude, DimUnidadeSaude.id_unidade == FatoIndicadorAPS.id_unidade)
        .join(DimIndicador, DimIndicador.id_indicador == FatoIndicadorAPS.id_indicador)
        .filter(DimMunicipio.codigo_ibge == codigo_ibge)
        .filter(FatoIndicadorAPS.periodo_referencia == periodo)
        .filter(DimIndicador.codigo == indicador)
        .group_by(
            DimUnidadeSaude.id_unidade,
            DimUnidadeSaude.codigo_cnes,
            DimUnidadeSaude.nome,
            DimUnidadeSaude.latitude,
            DimUnidadeSaude.longitude,
        )
        .order_by(DimUnidadeSaude.id_unidade)
    )
    results = query.all()
    duration_ms = (perf_counter() - start) * 1000
    logger.info(
        "[PERF] service=listar_indicador_geo_unidade municipio={} indicador={} periodo={} rows={} duration_ms={:.2f}",
        codigo_ibge,
        indicador,
        periodo,
        len(results),
        duration_ms,
    )
    return [IndicadorUnidadeGeoOut(**dict(row._mapping)) for row in results]


def listar_indicador_geo_territorio(
    db: Session, codigo_ibge: str, indicador: str, periodo: str
) -> List[IndicadorTerritorioGeoOut]:
    start = perf_counter()
    query = (
        db.query(
            DimTerritorio.id_territorio.label("id_territorio"),
            DimTerritorio.codigo_territorio.label("codigo_territorio"),
            DimTerritorio.descricao.label("descricao"),
            DimTerritorio.latitude.label("latitude"),
            DimTerritorio.longitude.label("longitude"),
            func.avg(FatoIndicadorAPS.valor).label("valor_indicador"),
            func.avg(FatoIndicadorAPS.meta).label("meta"),
            func.max(func.coalesce(FatoIndicadorAPS.atingiu_meta, False)).label("atingiu_meta"),
        )
        .join(DimMunicipio, DimMunicipio.id_municipio == FatoIndicadorAPS.id_municipio)
        .join(DimTerritorio, DimTerritorio.id_territorio == FatoIndicadorAPS.id_territorio)
        .join(DimIndicador, DimIndicador.id_indicador == FatoIndicadorAPS.id_indicador)
        .filter(DimMunicipio.codigo_ibge == codigo_ibge)
        .filter(FatoIndicadorAPS.periodo_referencia == periodo)
        .filter(DimIndicador.codigo == indicador)
        .group_by(
            DimTerritorio.id_territorio,
            DimTerritorio.codigo_territorio,
            DimTerritorio.descricao,
            DimTerritorio.latitude,
            DimTerritorio.longitude,
        )
        .order_by(DimTerritorio.id_territorio)
    )
    results = query.all()
    duration_ms = (perf_counter() - start) * 1000
    logger.info(
        "[PERF] service=listar_indicador_geo_territorio municipio={} indicador={} periodo={} rows={} duration_ms={:.2f}",
        codigo_ibge,
        indicador,
        periodo,
        len(results),
        duration_ms,
    )
    return [IndicadorTerritorioGeoOut(**dict(row._mapping)) for row in results]
