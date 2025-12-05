from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ...core.security import ensure_user_can_access_municipio, get_current_user
from ...db.session import get_db
from ...models.app import Usuario
from ...schemas.indicadores import IndicadorAPSOut
from ...services.indicadores_service import listar_indicadores

router = APIRouter()


@router.get(
    "/{codigo_ibge_municipio}",
    response_model=List[IndicadorAPSOut],
    summary="Retorna indicadores APS para um município",
)
def obter_indicadores(
    codigo_ibge_municipio: str,
    indicador: Optional[str] = Query(None, description="Código do indicador (ex.: C1, C2)"),
    periodo: Optional[str] = Query(None, description="Período de referência (ex.: 2025Q1, 2025M03)"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    ensure_user_can_access_municipio(current_user, codigo_ibge_municipio, db)
    return listar_indicadores(db, codigo_ibge=codigo_ibge_municipio, indicador=indicador, periodo=periodo)
