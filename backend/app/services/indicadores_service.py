from time import perf_counter
from typing import List, Optional

from loguru import logger
from sqlalchemy.orm import Session

from ..models.dw import DimIndicador, DimMunicipio, FatoIndicadorAPS
from ..schemas.indicadores import IndicadorAPSOut


def listar_indicadores(
    db: Session, codigo_ibge: str, indicador: Optional[str] = None, periodo: Optional[str] = None
) -> List[IndicadorAPSOut]:
    start = perf_counter()
    query = (
        db.query(
            DimMunicipio.nome.label("municipio"),
            DimMunicipio.codigo_ibge.label("codigo_ibge"),
            DimIndicador.codigo.label("indicador"),
            DimIndicador.nome.label("nome_indicador"),
            FatoIndicadorAPS.periodo_referencia.label("periodo_referencia"),
            FatoIndicadorAPS.valor.label("valor"),
            FatoIndicadorAPS.meta.label("meta"),
            FatoIndicadorAPS.atingiu_meta.label("atingiu_meta"),
        )
        .join(DimMunicipio, DimMunicipio.id_municipio == FatoIndicadorAPS.id_municipio)
        .join(DimIndicador, DimIndicador.id_indicador == FatoIndicadorAPS.id_indicador)
        .filter(DimMunicipio.codigo_ibge == codigo_ibge)
    )

    if indicador:
        query = query.filter(DimIndicador.codigo == indicador)

    if periodo:
        query = query.filter(FatoIndicadorAPS.periodo_referencia == periodo)

    query = query.order_by(FatoIndicadorAPS.periodo_referencia, DimIndicador.codigo)
    results = query.all()
    duration_ms = (perf_counter() - start) * 1000
    logger.info("[PERF] service=listar_indicadores municipio={} rows={} duration_ms={:.2f}", codigo_ibge, len(results), duration_ms)
    return [IndicadorAPSOut(**dict(row._mapping)) for row in results]
