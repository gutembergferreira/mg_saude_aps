from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ...db.session import get_db
from ...schemas.geoprocessamento import (
    IndicadorTerritorioGeoOut,
    IndicadorUnidadeGeoOut,
    UnidadeGeoOut,
)
from ...services.geoprocessamento_service import (
    listar_indicador_geo_territorio,
    listar_indicador_geo_unidade,
    listar_unidades_geo,
)

router = APIRouter()


@router.get("/unidades/{codigo_ibge_municipio}", response_model=List[UnidadeGeoOut])
def map_unidades(codigo_ibge_municipio: str, db: Session = Depends(get_db)):
    return listar_unidades_geo(db, codigo_ibge=codigo_ibge_municipio)


@router.get("/indicador/{codigo_ibge_municipio}")
def heatmap_indicador(
    codigo_ibge_municipio: str,
    indicador: str = Query(..., description="Código do indicador (ex: C1)"),
    periodo: str = Query(..., description="Período de referência (ex: 2025Q1)"),
    nivel: str = Query("unidade", description='Nível de agregação: "unidade" ou "territorio"'),
    db: Session = Depends(get_db),
):
    if nivel not in {"unidade", "territorio"}:
        raise HTTPException(status_code=400, detail='Parâmetro "nivel" deve ser "unidade" ou "territorio"')

    if nivel == "unidade":
        data = listar_indicador_geo_unidade(db, codigo_ibge=codigo_ibge_municipio, indicador=indicador, periodo=periodo)
        return [item.dict() for item in data]

    data = listar_indicador_geo_territorio(db, codigo_ibge=codigo_ibge_municipio, indicador=indicador, periodo=periodo)
    return [item.dict() for item in data]
